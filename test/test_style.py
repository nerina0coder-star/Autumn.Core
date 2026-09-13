import unittest

from Autumn import new
from Autumn.base import current_base


class Test(unittest.TestCase):
    def setUp(self):
        with new():
            self.style = current_base.style
            self.name = current_base.name

    def test_style_naming_for_names_identifiers_and_classes(self):

        name = self.name

        class Style(self.style.Style):
            def __init__(self):
                self.name = ["div.cls#id",
                             name.Name("p"),
                             name.Name("p", "identifier", ["cls"]),
                             ]

                super().__init__()

        class Style2(self.style.Style):
            def __init__(self):
                self.classes = ["cls1", "cls2", name.Class("cls 3")]

                super().__init__()

        class Style3(self.style.Style):
            def __init__(self):
                self.identifier = ["identifier", name.Identifier("identifier 2")]

                super().__init__()

        self.assertEqual(Style().build(), "div.cls#id,p,p#identifier.cls{}")
        self.assertEqual(Style2().build(), ".cls1,.cls2,.cls-3{}")
        self.assertEqual(Style3().build(), "#identifier,#identifier-2{}")
