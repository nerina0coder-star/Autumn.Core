import copy
import threading

from markupsafe import escape

from Autumn.Naming.class_ import Class
from Autumn.Naming.identifier import Identifier
from Autumn.abstract_base import AbstractBase


class Name(AbstractBase):
    """
    Represents a CSS name.
    """

    def __init__(self,
                 name,
                 /,
                 id_="",
                 classes=None,
                 *,
                 attributes = None):
        """
        :param attributes: CSS/JS only
        """
        if classes is None:
            classes = []

        self.name = name
        self.identifier = id_
        self.classes = classes

        self.attrs = attributes

        self._lock = threading.Lock()

        self._cache = []

    def build(self, cache_if_possible = True, **kwargs):

        out = [self.name]

        self.before_build(**kwargs)

        if self.identifier:
            identifier = self.identifier
            if isinstance(identifier, str):
                identifier = Identifier(identifier)
            out.append(f"#{identifier}")

        if self.classes:
            for cls in self.classes:
                if isinstance(cls, str):
                    cls = Class(cls)
                out.append(f".{cls}")

        if self.attrs:
            for k, v in self.attrs.items():
                out.append(f'[{escape(k)}="{escape(v)}"]')

        return ''.join(out)

    @staticmethod
    def from_tag(tag):
        return Name(tag.name, tag.identifier, copy.deepcopy(tag.classes))