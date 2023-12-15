from playwright.sync_api import BrowserContext, Page

from osbot_playwright.html_parser.Html_Parser import Html_Parser
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Misc import obj_info

TMP_FILE__PLAYWRIGHT_SCREENSHOT = '/tmp/playwright_screenshot.png'

class Playwright_Page:

    def __init__(self, context, page):
        self.context           : BrowserContext            = context
        self.page              : Page                      = page
        self.captured_requests : list                      = []

    def __repr__(self):
        return f'[Playwright_Page]: {self.page.url}'

    def capture_requests(self):
        def capture_request(request):
            captured_request = { 'frame'          : {'name': request.frame.name,
                                                     'url': request.frame.url  } ,
                                 'headers'        : request.headers              ,
                                 'method'         : request.method               ,
                                 'post_data'      : request.post_data            ,
                                 'post_data_json' : request.post_data_json       ,
                                 'redirected_from': request.redirected_from      ,
                                 'redirected_to'  : request.redirected_to        ,
                                 'resource_type'  : request.resource_type        ,
                                 'timing'         : request.timing               ,
                                 'url'            : request.url                  }
            self.captured_requests.append(captured_request)
        self.page.on("requestfinished", capture_request)

        # todo: add support for more events
        #
        # close             : Emitted when the page is closed.
        # console           : Emitted when a console message is logged in the page.
        # dialog            : Emitted when a dialog appears on the page (alert, prompt, confirm, or beforeunload).
        # domcontentloaded  : Emitted when the DOMContentLoaded event is fired.
        # download          : Emitted when a download begins on the page.
        # error             : Emitted when an uncaught exception happens within the page.
        # frameattached     : Emitted when a frame is attached to the page.
        # framedetached     : Emitted when a frame is detached from the page.
        # framenavigated    : Emitted when a frame is navigated to a new URL.
        # load              : Emitted when the load event is fired (the page is fully loaded).
        # pageerror         : Emitted when an uncaught exception happens within the page and is bubbled up to the window object.
        # popup             : Emitted when a new page is created by window.open or when a link with target=_blank is clicked.
        # request           : Emitted when a network request is made by the page.
        # requestfailed     : Emitted when a network request fails.
        # requestfinished   : Emitted when a network request is successfully completed.
        # response          : Emitted when a network response is received.
        # websocket         : Emitted when the page creates a WebSocket connection.
        # worker            : Emitted when a Web Worker is created by the page.

    def close(self):
        return self.page.close()

    def closed(self):
        return self.page.is_closed()

    def goto(self, *args, **kwargs):
        return self.page.goto(*args, **kwargs)

    def json(self):
        return self.html().json()

    def html_raw(self):
        return self.page.content()

    def html(self):
        return Html_Parser(self.html_raw())

    def title(self):
        return self.page.title()

    def open(self, url, **kwargs):
        return self.goto(url, **kwargs)

    def open__google(self, path):
        return self.open('https://www.google.com/' + path)

    def screenshot(self, **kwargs):
        if 'path' not in kwargs:
            kwargs['path'] = TMP_FILE__PLAYWRIGHT_SCREENSHOT
        self.screenshot_bytes(**kwargs)
        return kwargs['path']

    def screenshot_bytes(self, **kwargs):
        return self.page.screenshot(**kwargs)

    def set_html(self, html):
        self.page.set_content(html)
        return self
    def url(self):
        return self.page.url

    # todo: add method to wrap this selector
    # def get_images(page):
    #     # This function will run in the browser and collect image sources
    #     images = page.query_selector_all("img")
    #     image_urls = [page.evaluate(f"() => document.images[{index}].src", image) for index, image in
    #                   enumerate(images)]
    #     return image_urls
