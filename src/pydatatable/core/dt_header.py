from dataclasses import dataclass

@dataclass(frozen=True)
class DTHeader:
    """DTHeader"""
    name: str
    index: int
