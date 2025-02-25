import os
from abc import ABC, abstractmethod

class ReadingStrategy(ABC):
    """ReadingStrategy"""
    def __init__(self, path: str, **kwargs):
        self._path = path
        self._sheet_name = kwargs.get("sheet_name")
        self._encoding = kwargs.get("encoding", "utf-8")

    @abstractmethod
    def read(self) -> list[dict[str, str]]:
        """read"""

    def _file_exists(self):
        return os.path.exists(self._path)
