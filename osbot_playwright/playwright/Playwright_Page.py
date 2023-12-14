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


    def open(self, url, **kwargs):
        return self.goto(url, **kwargs)

    def screenshot(self, **kwargs):
        if 'path' not in kwargs:
            kwargs['path'] = TMP_FILE__PLAYWRIGHT_SCREENSHOT
        self.screenshot_bytes(**kwargs)
        return kwargs['path']

    def screenshot_bytes(self, **kwargs):
        return self.page.screenshot(**kwargs)


    def url(self):
        return self.page.url

    # todo: add method to wrap this selector
    # def get_images(page):
    #     # This function will run in the browser and collect image sources
    #     images = page.query_selector_all("img")
    #     image_urls = [page.evaluate(f"() => document.images[{index}].src", image) for index, image in
    #                   enumerate(images)]
    #     return image_urls
