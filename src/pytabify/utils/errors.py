class pytabifyError(Exception):
    """pytabifyError"""

class FileNotFoundException(pytabifyError):
    """FileNotFoundException"""

class FileReadingException(pytabifyError):
    """FileReadingException"""

class FileWritingException(pytabifyError):
    """FileWritingException"""

class FileExtensionException(pytabifyError):
    """FileReadingException"""

class SheetNameHasNotEmptyException(pytabifyError):
    """SheetNameHasNotEmptyException"""

class SheetNameDoesNotExistException(pytabifyError):
    """SheetNameDoesNotExistException"""