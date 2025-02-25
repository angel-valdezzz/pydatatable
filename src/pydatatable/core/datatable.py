from pydatatable.core.dt_row import DTRow
from pydatatable.utils.observer import FieldChangeObserver
from pydatatable.core.dt_header import DTHeader

class DataTable:
    """TestData"""
    def __init__(self, rows: list[DTRow], observer: FieldChangeObserver):
        self._rows = rows
        self._len = len(rows)
        self._observer = observer

    def __len__(self):
        return len(self._rows)

    def row(self, index: int) -> DTRow:
        """row"""
        return self._rows[index]

    def total_rows(self):
        """total_rows"""
        return self._len

    def __getitem__(self, index: int):
        return self._rows[index]

    def __iter__(self):
        return iter(self._rows)

    def headers(self):
        """headers"""
        return list(
            {DTHeader(field.name, field.index) for row in self._rows for field in row}
              | {DTHeader(event["field"].name, event["pos"]) for event in self._observer.events}
        )

    def to_dict(self):
        """to_dict"""
        return [row.to_dict() for row in self._rows]
