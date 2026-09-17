import dataclasses
import threading

from markupsafe import escape


@dataclasses.dataclass(frozen=True)
class Class:
    """
    The class used to hold CSS/HTML class names.
    """
    name: str

    _lock = threading.Lock()

    def __post_init__(self):
        if not len(self.name) > 0 or self.name[0].isdigit():
            raise ValueError("Class name must not be empty and must not start with a digit.")
        object.__setattr__(self, "name", escape(self.name))

    def __str__(self):
        with self._lock:
            return self.name.replace(" ", "-").replace("\n", "-").replace("\t", "-")