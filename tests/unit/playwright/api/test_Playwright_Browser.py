from asyncio import unix_events
from unittest import TestCase
from unittest.mock import patch
from osbot_utils.utils.Files import file_exists
from playwright.sync_api import Playwright, BrowserType, Page, Error, BrowserContext

from osbot_playwright.playwright.api.Playwright_Browser import Playwright_Browser
from osbot_playwright.playwright.api.Playwright_Browser__Chrome import Playwright_Browser__Chrome
from osbot_playwright.playwright.api.Playwright_Install import SUPORTTED_BROWSERS
from osbot_playwright.playwright.api.Playwright_Page import Playwright_Page


class test_Playwright_Browser(TestCase):
    headless                  : bool
    playwright_browser        : Playwright_Browser
    playwright_browser_chrome : Playwright_Browser__Chrome

    @classmethod
    def setUpClass(cls) -> None:
        cls.headless = True
        cls.playwright_browser_chrome = Playwright_Browser__Chrome(headless=cls.headless)
        cls.playwright_browser        = cls.playwright_browser_chrome.playwright_browser()


    @classmethod
    def tearDownClass(cls) -> None:
        assert cls.playwright_browser_chrome.stop_playwright_and_process() is True

    def test_browser_via_cdp(self):
        assert self.playwright_browser.browser_via_cdp(browser_name=None, endpoint_url=None) is None

    def test_browser_type(self):
        for browser in SUPORTTED_BROWSERS:
            assert type(self.playwright_browser.browser_type(browser)) is BrowserType
        assert self.playwright_browser.browser_type('aaa') is None

    def test_contexts_close_all(self):
        with self.playwright_browser as _:
            assert len(_.contexts()     ) == 1
            assert len(_.pages()        ) == 0
            assert type(_.new_page()    ) == Playwright_Page
            assert len(_.pages()        ) == 1
            assert type(_.context_new() ) == BrowserContext
            assert len(_.contexts()     ) == 2

            assert _.contexts_close_all() == 2
            assert len(_.pages()        ) == 0
            assert len(_.contexts()     ) == 0

            # simulate when close_context raises an exception
            with patch.object(_, 'context_close', side_effect=Error("Test exception")):
                _.contexts_close_all()

        assert self.playwright_browser_chrome.restart() is True         # need to restart since after closing all contexts, creating a new one throws an error (saying that the browser has been closed)
        assert len(self.playwright_browser.contexts())  == 1
        assert len(self.playwright_browser.pages())     == 0
            #_.restart_process()

    def test_context_new(self):
        with self.playwright_browser as _:
            assert len(_.contexts()) == 1
            kwargs = dict( viewport                 = None ,
                           screen                   = None ,
                           extra_http_headers       = None ,
                           java_script_enabled      = None ,
                           record_har_path          = None ,
                           record_har_omit_content  = None ,
                           record_har_url_filter    = None ,
                           record_har_mode          = None ,
                           record_har_content       = None ,
                           record_video_dir         = None ,
                           record_video_size        = None ,
                           base_url                 = None )
            new_context = _.context_new(**kwargs)
            assert len(_.contexts()) == 2
            new_context.close()
            assert len(_.contexts()) == 1

    def test_event_loop(self):
        def create_and_stop():
            event_loop = self.playwright_browser.event_loop()
            assert type(event_loop) is unix_events._UnixSelectorEventLoop
            assert event_loop.is_running() is True
            assert event_loop.is_closed () is False
            assert event_loop.slow_callback_duration == 0.1

            assert self.playwright_browser.stop() is True
            assert event_loop.is_running       () is False
            assert event_loop.is_closed        () is True

            assert self.playwright_browser.event_loop() is None
            assert self.playwright_browser.playwright() is not None  # this will create the event loop
            assert self.playwright_browser.event_loop() is not None


        assert self.playwright_browser.playwright() is not None  # this will create the event loop

        create_and_stop()                   # try this twice to make sure we can start, stop and start
        create_and_stop()                   # the main playwright event loop

        assert self.playwright_browser_chrome.restart() is True         # todo: figure out why we need to restart it here
        page = self.playwright_browser.new_page()                       #       without the restart, we get an error saying that the eventloop is closed (which feels like the wrong message)
        assert type(page) is Playwright_Page
        assert page.close() is True



    def test_playwright(self):
        #print()

        playwright = self.playwright_browser.playwright()
        assert type(playwright) is Playwright

        #obj_info(playwright, value_width=512)

        assert len(playwright.devices  ) > 100
        assert type(playwright.chromium) is BrowserType
        assert type(playwright.firefox ) is BrowserType
        assert type(playwright.webkit  ) is BrowserType

        assert file_exists(playwright.chromium.executable_path) is True
        assert file_exists(playwright.firefox .executable_path) is False        # todo add support for Firefox
        assert file_exists(playwright.webkit  .executable_path) is False        # todo add support for WebKit



    def test_new_page(self):
        assert len(self.playwright_browser.pages()) == 0
        page = self.playwright_browser.new_page()
        assert len(self.playwright_browser.pages()) == 1
        assert type(page)                           is Playwright_Page
        assert page.url      ()                     == 'about:blank'
        assert self.playwright_browser.page().page  == page.page
        assert page.is_closed()                     is False
        assert page.close    ()                     is True
        assert page.is_closed()                     is True
        assert len(self.playwright_browser.pages()) == 0

    def test_page(self):
        assert len(self.playwright_browser.pages()) == 0
        target_url     = 'https://www.google.com/404'
        expected_title = 'Error 404 (Not Found)!!1'
        page = self.playwright_browser.page()
        assert len(self.playwright_browser.pages()) == 1
        assert type(page)                           is Playwright_Page
        assert page.url      ()                     == 'about:blank'
        assert page.open     (target_url).url       == target_url
        assert page.url      ()                     == target_url
        assert page.html     ().title()             == expected_title
        assert page.is_closed()                     is False
        assert self.playwright_browser.page().page  == page.page
        assert page.close    ()                     is True
        assert page.is_closed()                     is True
        assert len(self.playwright_browser.pages()) == 0


    def test_playwright_context_manager(self):
        self.playwright_browser.stop()
        playwright_context_manager = self.playwright_browser.playwright_context_manager()
        assert playwright_context_manager._exit_was_called  is False
        assert playwright_context_manager._own_loop         is False
        assert playwright_context_manager._watcher          is None


        playwright = playwright_context_manager.start()

        assert playwright_context_manager._exit_was_called  is False
        assert playwright_context_manager._own_loop         is True
        assert playwright_context_manager._watcher          is None

        playwright.stop()

        assert playwright_context_manager._exit_was_called is True
        assert playwright_context_manager._own_loop        is True
        assert playwright_context_manager._watcher         is None


    # def test_video_recording(self):
    #     browser = self.api_playwright.browser()
    #     #page = self.api_playwright.page()
    #     record_video_dir = '/tmp/videos'
    #     context = browser.new_context(record_video_dir=record_video_dir)
    #     pprint(context)
    #     page = context.new_page()
    #     page.goto('https://news.bbc.co.uk')
    #
    #     for i in range(0,10):
    #         page.mouse.wheel(0, 100)
    #         #page.keyboard.press('PageDown')
    #         #wait_for(0.5)
    #     page.close()
    #     context.close()

    # @sync
    # async def test_page(self):
    #     page = await self.api_playwright.page()
    #     assert type(page) is Page
    #     assert str(page)  == "<Page url='about:blank'>"
    #
    # def test_url(self):
    #     assert self.api_playwright.url() == 'about:blank'
    #
    # @sync
    # async def test_connect_over(self):
    #     playwright = await async_playwright().start()
    #     browser = await playwright.chromium.connect_over_cdp("http://localhost:9222")
    #     page = await browser.new_page()
    #     pprint(page.url)
    #
    #     await page.goto("https://www.google.com/404")
    #
    #     aa = 13
    #
    #     # return
    #     # self.log_info("before sync_playwright")
    #     # from playwright.sync_api import sync_playwright
    #     # with sync_playwright() as playwright:
    #     #     self.log_info("in with sync_playwright")
    #     #     browser = playwright.chromium.launch()
    #     #     self.log_info("got browser")
    #     #     context = browser.new_context()
    #     #     self.log_info("got context")
    #     #     page = context.new_page()
    #     #     self.log_info("got new page")
    #     #     page.goto("https://google.com")
    #     #     self.log_info("opened google.com")
    #     #     self.log_info("saving screenshot")
    #     #     content = page.content()
    #     #     html = page.inner_html("*")
    #     #     text = page.inner_text("*")
    #     #     self.log_info(f"got page content with size {len(content)}")
    #     #     self.log_info(f"got page html with size {len(html)}")
    #     #     self.log_info(f"got page text with size {len(text)}")
    #     #     page.screenshot(path="/tmp/browser_screenshot.png")
    #     #     self.log_info("saved screenshot")
    #     #     browser.close()
    #     #     self.log_info("brower closed")
    #
    # @sync
    # async def test_connect_over(self):
    #     playwright = await async_playwright().start()
    #     browser = await playwright.chromium.connect_over_cdp("http://localhost:9222")
    #     default_context = browser.contexts[0]
    #     page            = default_context.pages[0]
    #     #page = await browser.new_page()
    #     #await default_context.new_page()
    #     #await page.goto("https://www.google.com")
    #     #pprint(page.url)
    #
    # # page.goto("https://www.google.com")
    # # page.goto("https://www.google.com")
    # # page.fill('textarea[name="q"]', 'owasp')
    # # page.press('textarea[name="q"]', 'Enter')
    # # page.wait_for_load_state('networkidle')
    #
    # # links = page.query_selector_all('a')
    # # for link in links:
    # #     url = link.get_attribute('href')
    # #     if url:
    # #         print(url)
    #
    # # print()
    # # #pprint(page.query_selector_all('textarea[name="q"]'))
    # # inputs = page.query_selector_all('textarea')
    # #
    # # for input_element in inputs:
    # #     # Get the value of the input element
    # #     value = input_element.input_value()
    # #     print(f"Input value: {value}")
    # #
    # #     # Get the type of the input element
    # #     input_type = input_element.get_attribute('type')
    # #     print(f"Input type: {input_type}")
    # # path="/tmp/browser_screenshot.png"
    # # pprint(len(page.screenshot(type='jpeg', quality=0, path=path)))
    #
    # # pprint(self.playwright_chrome_browser.page())
    #     # context = self.playwright_chrome_browser.context().new_page()
    #     # for page in self.playwright_chrome_browser.pages():
    #     #     page.bring_to_front()
    #     #     wait_for(1)
    #     #page.goto('http://news.bbc.co.uk')
    #     #page.close()
    #     # browser.new_page()
    #     # return
