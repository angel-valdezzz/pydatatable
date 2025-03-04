import os
from typing import Any
from pydatatable.core.datatable import DataTable
from pydatatable.core.dt_row import DTRow
from pydatatable.core.dt_field import DTField
from pydatatable.io.file_formats import FileFormats
from pydatatable.utils.observer import FieldChangeObserver
from pydatatable.utils.validation import validate_data
from pydatatable.utils.errors import FileExtensionException

class DataTableCreator:
    """Permite crear un DataTable a partir de un archivo o de una lista de diccionarios.
    
    Ejemplo:

    ```python
    from pydatatable import DataTableCreator

    dt = DataTableCreator.from_file("data.json")
    dt = DataTableCreator.from_records([{"name": "Alice", "age": 30}])
    ```

    Notas:
    - El archivo debe tener una extension valida (.csv, .json, .xlsx).
    - La lista de diccionarios debe tener la misma estructura (lista de diccionarios).
    - Para lectura de archivos XLSX se debe especificar el nombre de la hoja con el argumento sheet_name.
    """

    @staticmethod
    def from_file(path: str, **kwargs) -> DataTable:
        """Crea un DataTable a partir de un archivo."""
        data = DataTableCreator._read_data(path, **kwargs)
        return DataTableCreator._create_dt(data)

    @staticmethod
    def from_records(records: list[dict[str, Any]]) -> DataTable:
        """Crea un DataTable a partir de una lista de diccionarios."""
        return DataTableCreator._create_dt(records)

    @staticmethod
    def _read_data(path, **kwargs):
        _, ext_file = os.path.splitext(path)
        if ext_file not in FileFormats:
            raise FileExtensionException(f"La extension {ext_file} no es valida.")
        reading_strategy = FileFormats(ext_file).get_strategy()
        data = reading_strategy(path, **kwargs).read()
        validate_data(data)
        return data

    @staticmethod
    def _create_dt(data):
        observer = FieldChangeObserver()
        rows = [
            DTRow(
                fields=[
                    DTField(name, value, index)
                    for index, (name, value) in enumerate(record.items())
                ],
                index=row_index,
                observer=observer
            )
            for row_index, record in enumerate(data)
        ]

        return DataTable(rows, observer)
