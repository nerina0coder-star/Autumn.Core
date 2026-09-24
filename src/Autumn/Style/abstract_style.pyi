import abc
import threading
from typing import Any

from Autumn.Naming import Name, Class
from Autumn.Naming.identifier import Identifier
from Autumn.Style.Styles.style_holder import StyleHolder
from Autumn.abstract_base import AbstractBase


class AbstractStyle(AbstractBase, abc.ABC):

    name: list[Name | str]
    identifier: list[Identifier | str]
    classes: list[Class | str]
    styles: list[StyleHolder | str]
    dynamic: bool
    worth: int | Any
    _cache: list[str]
    _lock: threading.RLock

    def __init__(self) -> None: ...

    def build(self, cache_if_possible: bool = True, **kwargs: Any) -> str: ...
    
    def __eq__(self, other: AbstractStyle) -> bool: ... # type: ignore[override]

    def __ne__(self, other: AbstractStyle) -> bool: ... # type: ignore[override]

    def __lt__(self, other: AbstractStyle) -> bool: ...

