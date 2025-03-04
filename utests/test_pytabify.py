import os
import sys
import pytest
from assertpy import assert_that
from unittest.mock import MagicMock, patch, mock_open

path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.append(path)

from pytabify import (
    DataTableCreator,
    DataTableSaver,
    DataTable
)
from pytabify.core.dt_row import DTRow
from pytabify.core.dt_field import DTField
from pytabify.utils.observer import FieldChangeObserver
from pytabify.io.strategies.reading import (
    CSVFileReadingStrategy,
    JSONFileReadingStrategy,
    XLSXReadingStrategy
)
from pytabify.io.strategies.saving import (
    JsonFileSavingStrategy,
    CsvFileSavingStrategy
)
from pytabify.io.file_formats import FileFormats
from pytabify.utils.errors import (
    FileExtensionException,
    FileWritingException,
    SheetNameHasNotEmptyException,
    SheetNameDoesNotExistException
)

@pytest.fixture
def sample_records():
    return [
        {"name": "Alice", "age": 30},
        {"name": "Bob", "age": 25}
    ]

@pytest.fixture
def sample_datatable(sample_records):
    return DataTableCreator.from_records(sample_records)

class TestDataTableCreator:
    def test_from_records_crea_objeto_datatable(self, sample_records):
        dt = DataTableCreator.from_records(sample_records)
        assert_that(dt).is_instance_of(DataTable)
        assert_that(dt).is_length(2)
        assert_that(dt[0].name.value).is_equal_to("Alice")
        assert_that(dt[0].age.value).is_type_of(str)

    @patch("pytabify.creator.DataTableCreator._read_data", return_value=[{"country": "Spain"}])
    def test_from_file(self, mock_read):
        dt = DataTableCreator.from_file("dummy.json")
        assert_that(dt).is_instance_of(DataTable)
        assert_that(str(dt[0].country)).is_equal_to("Spain")
        mock_read.assert_called_once()

    def test_from_file_extension_invalida(self):
        with pytest.raises(FileExtensionException):
            DataTableCreator.from_file("archivo.txt")

class TestFileFormats:
    @pytest.mark.parametrize("ext, ext_class", [
        (".csv", CSVFileReadingStrategy),
        (".json", JSONFileReadingStrategy),
        (".xlsx", XLSXReadingStrategy)
    ])
    def test_get_strategy(self, ext, ext_class):
        strategy_class = FileFormats(ext).get_strategy()
        assert_that(strategy_class).is_equal_to(ext_class)

class TestDataTable:
    def test_len(self, sample_datatable):
        assert_that(sample_datatable).is_length(2)
        assert_that(sample_datatable.total_rows()).is_equal_to(2)

    def test_row_retorna_dtrrow(self, sample_datatable):
        row = sample_datatable.row(0)
        assert_that(row).is_instance_of(DTRow)
        assert_that(str(row.name)).is_equal_to("Alice")

    def test_headers(self, sample_datatable):
        headers = sample_datatable.headers()
        assert_that(any(h.name == "name" for h in headers)).is_true()
        assert_that(any(h.name == "age" for h in headers)).is_true()

    def test_to_dict(self, sample_datatable):
        data_dict = sample_datatable.to_dict()
        assert_that(data_dict).is_instance_of(list)
        assert_that(data_dict[0]).is_equal_to({"name": "Alice", "age": "30"})

class TestDTRow:
    def test_setitem(self):
        observer = FieldChangeObserver()
        row = DTRow([], 0, observer)
        row["city"] = "Madrid"
        assert row["city"].value == "Madrid"
        assert len(row) == 1
        assert len(observer.events) == 1

    def test_setattr(self):
        observer = FieldChangeObserver()
        row = DTRow([], 0, observer)
        row.country = "Mexico"
        assert_that(row.country.value).is_equal_to("Mexico")
        assert_that(row).is_length(1)
        assert_that(observer.events).is_length(1)

    def test_to_dict(self):
        observer = FieldChangeObserver()
        row = DTRow([], 0, observer)
        row["name"] = "Test"
        row["value"] = "123"
        dict_rep = row.to_dict()
        assert_that(dict_rep).is_equal_to({"name": "Test", "value": "123"})

class TestDTField:
    def test_is_empty(self):
        field = DTField("test", "", 0)
        assert_that(field.is_empty).is_true()

    def test_propiedades(self):
        field = DTField("edad", "20", 1)
        assert_that(field.name).is_equal_to("edad")
        assert_that(field.value).is_equal_to("20")
        assert_that(field.index).is_equal_to(1)
        assert_that(field).is_length(2)

class TestFieldChangeObserver:
    def test_notifica(self):
        observer = FieldChangeObserver()
        field = DTField("test", "xyz", 0)
        observer.notify(0, field)
        assert_that(observer.events).is_length(1)
        assert_that(observer.events[0]["field"].value).is_equal_to("xyz")

class TestReadingStrategies:
    @patch("builtins.open", new_callable=mock_open, read_data='[{"name": "Alice"}]')
    def test_json_reading_strategy(self, mock_file, tmp_path):
        filepath = tmp_path / "test.json"
        filepath.write_text('[{"name": "Alice"}]')
        strategy = JSONFileReadingStrategy(str(filepath))
        data = strategy.read()
        assert_that(data[0]["name"]).is_equal_to("Alice")

    @patch("builtins.open", new_callable=mock_open, read_data='name,age\nAlice,30\nBob,25\n')
    def test_csv_reading_strategy(self, mock_file, tmp_path):
        csv_content = "name,age\nAlice,30\nBob,25\n"
        filepath = tmp_path / "test.csv"
        filepath.write_text(csv_content)
        strategy = CSVFileReadingStrategy(str(filepath))
        data = strategy.read()
        assert_that(data[1]["age"]).is_equal_to("25")

    @patch("pytabify.io.strategies.reading.load_workbook")
    def test_xlsx_reading_strategy(self, mock_load_workbook, tmp_path):
        # Configurar el mock del workbook
        mock_workbook = MagicMock()
        mock_sheet = MagicMock()
        mock_workbook.__getitem__.return_value = mock_sheet  # Simula workbook["Sheet"]
        mock_workbook.active = mock_sheet
        mock_workbook.sheetnames = ["Sheet"]  # ¡Crucial! Incluye "Sheet" en sheetnames
        mock_load_workbook.return_value = mock_workbook

        # Configurar el mock de la hoja
        mock_sheet.__getitem__.return_value = [MagicMock(value="name"), MagicMock(value="age")]
        mock_sheet.iter_rows.return_value = [
            ("Alice", 30),
            ("Bob", 25)
        ]

        # Crear archivo temporal (aunque no se usa realmente gracias al mock)
        filepath = tmp_path / "test.xlsx"
        filepath.touch()

        # Ejecutar la estrategia
        strategy = XLSXReadingStrategy(str(filepath), sheet_name="Sheet")
        data = strategy.read()

        # Verificaciones
        assert len(data) == 2
        assert data[0]["name"] == "Alice"
        assert data[1]["age"] == "25"

    @patch("pytabify.io.strategies.reading.load_workbook")
    def test_xlsx_reading_strategy_sheet_name_does_not_exist(self, mock_load_workbook, tmp_path):
        # Configurar el mock del workbook
        mock_workbook = MagicMock()
        mock_workbook.sheetnames = ["Sheet1", "Sheet2"]  # Hojas existentes, pero no "SheetTest"
        mock_load_workbook.return_value = mock_workbook

        # Crear archivo temporal (opcional con el mock)
        filepath = tmp_path / "test.xlsx"
        filepath.touch()

        # Verificar que se lanza la excepción correcta
        with pytest.raises(SheetNameDoesNotExistException):
            XLSXReadingStrategy(str(filepath), sheet_name="SheetTest").read()

    @patch("pytabify.io.strategies.reading.load_workbook")
    def test_xlsx_reading_strategy_sheet_name_none(self, mock_load_workbook, tmp_path):
        # Configurar el mock del workbook (no se usa realmente porque falla antes)
        mock_workbook = MagicMock()
        mock_load_workbook.return_value = mock_workbook

        # Crear archivo temporal
        filepath = tmp_path / "test.xlsx"
        filepath.touch()

        # Verificar que se lanza la excepción correcta
        with pytest.raises(SheetNameHasNotEmptyException):
            XLSXReadingStrategy(str(filepath)).read()

class TestSaver:
    @patch("builtins.open", new_callable=mock_open)
    def test_into_json(self, mock_file, sample_datatable, tmp_path):
        output_file = tmp_path / "output.json"
        DataTableSaver.into_json(sample_datatable, str(output_file))
        handle = mock_file()
        handle.write.assert_called()

    @patch("builtins.open", new_callable=mock_open)
    def test_into_csv(self, mock_file, sample_datatable, tmp_path):
        output_file = tmp_path / "output.csv"
        DataTableSaver.into_csv(sample_datatable, str(output_file))
        handle = mock_file()
        handle.write.assert_called()

    def test_into_csv_error(self, sample_datatable, tmp_path):
        with patch("csv.DictWriter.writerow", side_effect=Exception("Error")):
            with pytest.raises(FileWritingException):
                CsvFileSavingStrategy.save(sample_datatable, str(tmp_path / "output.csv"), "utf-8")

    def test_into_json_error(self, sample_datatable, tmp_path):
        with patch("json.dump", side_effect=Exception("Error")):
            with pytest.raises(FileWritingException):
                JsonFileSavingStrategy.save(sample_datatable, str(tmp_path / "output.json"), "utf-8")
