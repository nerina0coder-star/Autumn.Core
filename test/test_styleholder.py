import unittest
from typing import Any

from Autumn import new


class Test(unittest.TestCase):
    def setUp(self):
        self.style = new().style

    def test_creating_styleholder(self):

        class Holder(self.style.holder):
            def __init__(self):
                self.name = "color"
                self.value = "red"
                self.important = True
                super().__init__()

        class Holder2(self.style.holder):
            def __init__(self):
                self.name = "color"
                self.value = "red"
                super().__init__()

        self.assertEqual(Holder().build(), "color:red!important;")
        self.assertEqual(Holder2().build(), "color:red;")

    def test_before_build_hook(self):
        called = []

        class Holder(self.style.holder):
            def __init__(self):
                self.name = "color"
                self.value = "red"
                super().__init__()

            def before_build(self, **kwargs: Any) -> str | None:
                called.append(True)
                assert kwargs == {}

        class Holder2(self.style.holder):
            def __init__(self):
                self.name = "color"
                self.value = "red"
                super().__init__()

            def before_build(self, **kwargs: Any) -> str | None:
                called.append(True)
                assert kwargs == {"test": "ing"}

        class Holder3(self.style.holder):
            def __init__(self):
                self.name = "color"
                self.value = "red"
                super().__init__()

            def before_build(self, **kwargs: Any) -> str | None:
                called.append(True)
                return "Hello World"

        self.assertEqual(Holder().build(), "color:red;")
        self.assertEqual(Holder2().build(test="ing"), "color:red;")
        self.assertEqual(Holder3().build(), "Hello World")
        self.assertEqual(called.count(True), 3)

    def test_caches(self):

        called = []

        class Holder(self.style.holder):
            def __init__(self):
                self.name = "color"
                self.value = "red"
                self.dynamic = False  # as said, the only class that needs explicit dynamic=False.
                super().__init__()

            def before_build(self, **kwargs: Any) -> str | None:
                called.append(True)

        holder = Holder()
        holder.build()
        holder.build()

        self.assertEqual(len(called), 1)
        self.assertEqual(called[0], True)
