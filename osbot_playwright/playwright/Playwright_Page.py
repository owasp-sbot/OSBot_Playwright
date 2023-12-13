from playwright.sync_api import BrowserContext, Page

from osbot_playwright.html_parser.Html_Parser import Html_Parser
from osbot_utils.utils.Dev import pprint

TMP_FILE__PLAYWRIGHT_SCREENSHOT = '/tmp/playwright_screenshot.png'

class Playwright_Page:

    def __init__(self, context, page):
        self.context : BrowserContext            = context
        self.page    : Page                      = page

    def __repr__(self):
        return f'[Playwright_Page]: {self.page.url}'

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

    def screenshot(self, **kwargs):
        if 'path' not in kwargs:
            kwargs['path'] = TMP_FILE__PLAYWRIGHT_SCREENSHOT
        self.screenshot_bytes(**kwargs)
        return kwargs['path']

    def screenshot_bytes(self, **kwargs):
        return self.page.screenshot(**kwargs)


    def url(self):
        return self.page.url