class PyDataTableError(Exception):
    """PyDataTableError"""

class FileNotFoundException(PyDataTableError):
    """FileNotFoundException"""

class FileReadingException(PyDataTableError):
    """FileReadingException"""

class FileWritingException(PyDataTableError):
    """FileWritingException"""

class FileExtensionException(PyDataTableError):
    """FileReadingException"""

class SheetNameHasNotEmptyException(PyDataTableError):
    """SheetNameHasNotEmptyException"""

class SheetNameDoesNotExistException(PyDataTableError):
    """SheetNameDoesNotExistException"""