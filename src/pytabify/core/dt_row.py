from pytabify.core.dt_field import DTField
from pytabify.utils.observer import FieldChangeObserver

class DTRow:
    """DTRow"""
    def __init__(self, fields: list[DTField], index: int, observer: FieldChangeObserver):
        self._fields = fields
        self._observer = observer
        self._index = index

    def __setitem__(self, name, value):
        new_index = self._observer.new_index()
        if new_index == 0:
            new_index = len(self._fields)

        field = DTField(name, value, new_index)
        self._fields.append(field)
        self._observer.notify(new_index, field)

    def __setattr__(self, name, value):
        if name.startswith("_"):
            super().__setattr__(name, value)
        else:
            new_index = self._observer.new_index()
            if new_index == 0:
                new_index = len(self._fields)

            field = DTField(name, value, new_index)
            self._fields.append(field)
            self._observer.notify(new_index, field)

    def __getitem__(self, name: str) -> DTField:
        values = list(filter(lambda field: field.name == name, self._fields))
        if values:
            return values[0]

    def __getattr__(self, name: str) -> DTField:
        values = list(filter(lambda field: field.name == name, self._fields))
        if values:
            return values[0]

    def __len__(self):
        return len(self._fields)

    def total_fields(self):
        """total_fields"""
        return len(self._fields)

    def to_dict(self):
        """to_dict"""
        return {field.name:field.value for field in self._fields}

    def __iter__(self):
        return iter(self._fields)
