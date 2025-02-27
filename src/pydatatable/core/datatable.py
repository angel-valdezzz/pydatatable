from pydatatable.core.dt_row import DTRow
from pydatatable.utils.observer import FieldChangeObserver
from pydatatable.core.dt_header import DTHeader

class DataTable:
    """Representa un conjunto de datos tabulares (filas y columnas).

    Cada fila es un objeto DTRow y cada columna es un objeto DTField.
    La primer fila es considerada como la fila de encabezados.
    Aunque la fila 0 es de encabezados, no se considera como una fila de datos y no se incluye en el conteo de filas, por lo que se puede acceder a la primer fila de datos con el indice 0.
    """

    def __init__(self, rows: list[DTRow], observer: FieldChangeObserver):
        self._rows = rows
        self._len = len(rows)
        self._observer = observer

    def __len__(self):
        return len(self._rows)

    def row(self, index: int) -> DTRow:
        """Obtiene una fila por su indice."""
        return self._rows[index]

    def total_rows(self):
        """Indica el total de filas de datos."""
        return self._len

    def __getitem__(self, index: int):
        return self._rows[index]

    def __iter__(self):
        return iter(self._rows)

    def headers(self):
        """Obtiene los encabezados de las columnas."""
        return list(
            {DTHeader(field.name, field.index) for row in self._rows for field in row}
              | {DTHeader(event["field"].name, event["pos"]) for event in self._observer.events}
        )

    def to_dict(self):
        """Convierte el DataTable a una lista de diccionarios."""
        return [row.to_dict() for row in self._rows]
