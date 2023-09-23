from osbot_playwright.html_parser.Html_Parser import Html_Parser


class Playwright_Page:

    def __init__(self, browser, context, page):
        self.browser = browser
        self.context = context
        self.page    = page

    def close(self):
        return self.page.close()

    def goto(self, *args, **kwargs):
        return self.page.goto(*args, **kwargs)

    def html_raw(self):
        return self.page.content()

    def html(self):
        return Html_Parser(self.html_raw())

    def title(self):
        return self.page.title()


    def open(self, url):
        return self.goto(url)

    def url(self):
        return self.page.url