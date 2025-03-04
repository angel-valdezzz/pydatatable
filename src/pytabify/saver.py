from pytabify.core.datatable import DataTable
from pytabify.io.strategies.saving import JsonFileSavingStrategy, CsvFileSavingStrategy, XlsxFileSavingStrategy

class DataTableSaver:
    """Permite guardar un DataTable en diferentes formatos

    Ejemplo:
    ```
    from pytabify import DataTableCreator, DataTableSaver
    dt = DataTableCreator.from_file("data.json")
    DataTableSaver.into_csv(dt, "data.csv")
    ```

    Notas:
    - Se puede especificar el encoding del archivo.
    """
    @staticmethod
    def into_csv(datatable: DataTable, path: str, encoding: str = "utf-8"):
        """Guarda un DataTable en un archivo CSV."""
        CsvFileSavingStrategy.save(datatable, path, encoding)

    @staticmethod
    def into_json(datatable: DataTable, path: str, encoding: str = "utf-8"):
        """Guarda un DataTable en un archivo JSON."""
        JsonFileSavingStrategy.save(datatable, path, encoding)

    @staticmethod
    def into_xlsx(datatable: DataTable, path: str, encoding: str = "utf-8"):
        """Guarda un DataTable en un archivo XLSX."""
        XlsxFileSavingStrategy.save(datatable, path, encoding)
