from unittest import TestCase

from osbot_playwright.html_parser.Html_Parser import Html_Parser


class test_Html_Parser(TestCase):


    def test_footer(self):
        data = '<footer>Test Footer</footer>'
        parser = Html_Parser(data)
        assert parser.footer() == 'Test Footer'

        data = '<div>Some content</div>'
        parser = Html_Parser(data)
        assert parser.footer() is None

    def test_title(self):
        data = '<title>Test Title</title>'
        parser = Html_Parser(data)
        assert parser.title() == 'Test Title'

        data = '<div>Some content</div>'
        parser = Html_Parser(data)
        assert parser.title() is None