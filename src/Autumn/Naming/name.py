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
        if self.name.count(" ") + self.name.count("\t") + self.name.count("\n") != 0 or any(i in self.name for i in "#.[]"):
            raise ValueError(f"Invalid CSS Tag Name: {self.name}")

        self.before_build(**kwargs)

        if self.identifier:
            identifier = self.identifier
            if isinstance(identifier, str):
                identifier = Identifier(identifier)
            out.append(f"#{identifier}")

        if self.classes:
            for cls in self.classes:
                if cls:
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

    """    @staticmethod
    def from_string(string):
        hashtags = string.count("#")
        dots = string.count(".")
        steep_brackets = string.count("[")
        if hashtags + dots + steep_brackets == 0:
            return Name(string)

        identifier = ""
        classes = []

        hashtag_index = -1
        class_indexes: list[int] = []
        steep_bracket_indexes: list[tuple[int, int]] = []

        last_class_index = 0
        last_steep_bracket_index = 0

        if hashtags != 0:
            if hashtags != 1:
                raise ValueError("A name can't have multiple Identifiers.")
            hashtag_index = string.index("#")

        if dots != 0:
            for _ in range(dots):
                class_indexes.append(string.index(".", last_class_index))
                last_class_index = class_indexes[-1] + 1

        if steep_brackets != 0:
            if string.count("]") != steep_brackets:
                raise ValueError(f"Invalid CSS Selector: {string}")
            for i in range(steep_brackets):
                steep_bracket_indexes.append((string.index("[", last_steep_bracket_index), string.index("]", last_steep_bracket_index)))
                last_steep_bracket_index = steep_bracket_indexes[-1][0] + 1

        def get_identifier() -> Identifier:
            largest_after_hashtag_index = -1
            largest_cls_after = next(filter(lambda x: x >hashtag_index, class_indexes))
            largest_steep_bracket_after = next(filter(lambda x: x[0] > hashtag_index, steep_bracket_indexes))[0]

            largest_after_hashtag_index = min(largest_cls_after, largest_steep_bracket_after)

            return Identifier(string[hashtag_index + 1:largest_after_hashtag_index])

        def get_classes() -> list[Class]:
    """ # TODO - complete this