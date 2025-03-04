from abc import ABC, abstractmethod
from pytabify.core.datatable import DataTable

class SavingStrategy(ABC):
    """SavingStrategy"""
    @staticmethod
    @abstractmethod
    def save(datatable: DataTable, path: str, encoding: str) -> list[dict[str, str]]:
        """save"""
