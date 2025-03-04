from enum import Enum
from pytabify.io.interfaces.read import ReadingStrategy
from pytabify.io.strategies.reading import CSVFileReadingStrategy, JSONFileReadingStrategy, XLSXReadingStrategy

class FileFormats(Enum):
    """FileFormats"""
    CSV = ".csv"
    JSON = ".json"
    XLSX = ".xlsx"

    def get_strategy(self) -> ReadingStrategy:
        """get_strategy"""
        mapping = {
            FileFormats.CSV: CSVFileReadingStrategy,
            FileFormats.JSON: JSONFileReadingStrategy,
            FileFormats.XLSX: XLSXReadingStrategy
        }
        return mapping.get(self)
