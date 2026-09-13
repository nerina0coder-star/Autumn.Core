import dataclasses
import threading


@dataclasses.dataclass(frozen=True)
class Identifier:

    name: str

    _lock: threading.Lock = threading.Lock()

    def __post_init__(self) -> None: ...

    def __str__(self) -> str: ...
