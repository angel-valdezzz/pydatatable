"""FieldChangeObserver"""
from pydatatable.core.dt_field import DTField

class FieldChangeObserver:
    """FieldChangeObserver"""
    def __init__(self):
        self._events: list[dict[str, str]] = []
        self._pos = 0

    def new_index(self) -> int:
        """new_index"""
        return self._pos

    def notify(self, index, field: DTField):
        """notify"""
        self._events.append({
            "field": field,
            "pos": index
        })
        if self._pos == 0:
            self._pos = index
        else:
            self._pos += 1

    @property
    def events(self):
        """events"""
        return self._events
