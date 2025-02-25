class DTField:
    """DTField"""
    def __init__(self, name: str, value: str, index: int):
        self._name = str(name)
        self._value = str(value)
        self._index = index
        self._len = len(str(value))

    def __str__(self):
        return self._value

    @property
    def is_none(self):
        """is_none"""
        return self._value is None

    @property
    def is_empty(self):
        """is_empty"""
        return self._value == ""

    @property
    def name(self):
        """name"""
        return self._name

    @property
    def value(self):
        """value"""
        return self._value

    @property
    def index(self):
        """index"""
        return self._index

    def __len__(self):
        return self._len

    @property
    def length(self):
        """length"""
        return self._len
