import unittest

from Autumn import new


class Test(unittest.TestCase):

    def setUp(self):
        self.name = new().name

    def test_identifier(self):

        identifier = self.name.Identifier("identifier")
        identifier_with_space = self.name.Identifier("identifier with space")

        with self.assertRaises(ValueError) as exc:
            identifier_starting_with_digit = self.name.Identifier("1dentifier starting with digit")

        self.assertEqual(str(exc.exception), "Identifier name must not be empty and must not start with a digit.")

        self.assertEqual(locals().get("identifier_starting_with_digit", None), None)
        self.assertEqual(str(identifier_with_space), "identifier-with-space")
        self.assertEqual(str(identifier), "identifier")

    def test_classes(self):

        cls = self.name.Class("class")
        cls_with_space = self.name.Class("class with space")

        with self.assertRaises(ValueError) as exc:
            cls_starting_with_digit = self.name.Class("3lass starting with digit")

        self.assertEqual(str(exc.exception), "Class name must not be empty and must not start with a digit.")

        self.assertEqual(locals().get("cls_starting_with_digit", None), None)
        self.assertEqual(str(cls_with_space), "class-with-space")
        self.assertEqual(str(cls), "class")
