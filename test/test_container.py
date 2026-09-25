import unittest

from Autumn import new # type: ignore[import-not-found]


class Test(unittest.TestCase):

    def setUp(self) -> None:
        base = new()

        self.page = base.page
        self.style = base.style
        self.tag = base.tag
        self.name = base.name

    def test_page(self) -> None:
        page = (self.page.require(self.tag.meta.Cdn("style", "https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.8/js/bootstrap.min.js"))
                .new("my-page"))

        # page.tag(self.tag.meta.Head())

        self.assertMultiLineEqual(page.build(),
                                  "<!DOCTYPE html>"
                                  '<html lang="en" dir="auto">'
                                  "<head>"
                                  '<meta charset="UTF-8">'
                                  '<meta name="viewport" content="width=device-width,initial-scale=1.0">'
                                  "<title>my-page</title>"
                                  '<link href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.8/js/bootstrap.min.js" rel="stylesheet">'
                                  '</head>'
                                  '</html>')

        class CustomPage(self.page.Page):  # type: ignore[misc,name-defined]
            ...

        page2 = CustomPage("my-page")

        page2.require(
            self.tag.meta.Cdn(
                "style",
                "https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.8/js/bootstrap.min.js"
            )
        )

        self.maxDiff = None

        self.page.register(CustomPage("page"))

        self.assertMultiLineEqual(page.build(),
                                  page2.build())

        self.assertMultiLineEqual(page.build(),
                                  self.page.build("my-page"))

    def test_sheet(self) -> None:

        name = self.name

        class Style(self.style.Style):  # type: ignore[misc,name-defined]
            def __init__(self) -> None:
                self.styles = ["margin: 1px;", "padding: 1px;"]
                self.name = ["div", name.Name("smt", "identifier", ["any"])]
                self.classes = ["margin-and-padding", name.Class("cls")]
                self.identifier = ["id1", name.Identifier("id2")]

                super().__init__()

        sheet = self.style.Sheet(Style(), Style())

        self.assertMultiLineEqual(sheet.build(),
                                  ("div,smt#identifier.any"
                                  ",.margin-and-padding,.cls"
                                  ",#id1,#id2{margin: 1px;padding: 1px;}") * 2)

    def test_sheet_sorting(self)-> None:

        class Style(self.style.Style):
            def __init__(self, worth: int) -> None:
                self.worth = worth
                self.styles = [f"worth: {worth};"]
                self.classes = ["testing"]
                super().__init__()

        sheet = self.style.Sheet(Style(1), Style(2), Style(4), Style(3), Style(6), Style(6))

        sheet.sort()

        self.assertMultiLineEqual(sheet.build(),
                                  ".testing{worth: 1;}.testing{worth: 2;}.testing{worth: 3;}.testing{worth: 4;}.testing{worth: 6;}.testing{worth: 6;}")

