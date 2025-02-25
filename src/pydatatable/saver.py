from pydatatable.core.datatable import DataTable
from pydatatable.io.strategies.saving import JsonFileSavingStrategy, CsvFileSavingStrategy, XlsxFileSavingStrategy

class DataTableSaver:
    """TestDataSaver"""
    @staticmethod
    def into_csv(datatable: DataTable, path: str, encoding: str = "utf-8"):
        """save_into_csv"""
        CsvFileSavingStrategy.save(datatable, path, encoding)

    @staticmethod
    def into_json(datatable: DataTable, path: str, encoding: str = "utf-8"):
        """save_into_json"""
        JsonFileSavingStrategy.save(datatable, path, encoding)

    @staticmethod
    def into_xlsx(datatable: DataTable, path: str, encoding: str = "utf-8"):
        """save_into_xlsx"""
        XlsxFileSavingStrategy.save(datatable, path, encoding)
