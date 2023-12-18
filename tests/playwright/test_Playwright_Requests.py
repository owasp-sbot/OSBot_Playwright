import asyncio
from unittest import TestCase

import playwright
from playwright.sync_api import sync_playwright

from osbot_playwright.playwright.API_Browserless import API_Browserless
from osbot_playwright.playwright.Playwright_Requests import Playwright_Requests
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import file_exists
from osbot_utils.utils.Json import json_save, json_load, json_save_file, json_load_file


class test_Playwright_Requests(TestCase):
    api_browserless : API_Browserless

    @classmethod
    def setUpClass(cls) -> None:
        cls.api_browserless = API_Browserless()
        cls.page            = cls.api_browserless.new_page()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.api_browserless.close()

    def setUp(self) -> None:
        self.playwrite_requests = Playwright_Requests()

    def test__page__capture_requests(self):
        with self.page as _:
            _.open__google(404)
            assert len(_.requests.requests) == 0
            _.capture_requests()
            _.refresh()
            assert len(_.requests.requests) == 3

    def test_capture_request(self):
        with self.page as _:
            _.capture_requests()
            _.open__google(404)
            requests = _.requests.requests
            cache_file = json_save_file(_.requests.requests)
            pprint(cache_file)

    def test_load_from(self):
        file_with_captured_requests = '/var/folders/sj/ks1b_pjd749gk5ssdd1769kc0000gn/T/tmp299iiu8o.tmp'
        assert len(self.playwrite_requests.requests) == 0
        #requests = json_load_file(file_with_captured_requests)
        #pprint(requests)
        self.playwrite_requests.load_from(file_with_captured_requests)
        assert len(self.playwrite_requests.requests) > 0
        assert self.playwrite_requests.requests == json_load_file(file_with_captured_requests)

    def test_save_to(self):
        with self.page as _:
            _.capture_requests()
            _.open__google(404)

            path_requests = _.requests.save_to()
            assert file_exists(path_requests)
            assert _.requests.requests == json_load_file(path_requests)
            _.requests.requests = []
            assert len(_.requests.requests) == 0
            assert _.requests.load_from(path_requests)
            assert len(_.requests.requests) == 3
            assert _.requests.requests == json_load_file(path_requests)


        # class test_Playwright_close_bug(TestCase):
#     api_browserless : API_Browserless()
#
#     @classmethod
#     def setUpClass(cls) -> None:
#         cls.api_browserless = API_Browserless()
#         cls.wss_url         = cls.api_browserless.wss_url()



    # def test_replicate_bug(self):
    #     def request_finished_handler(request):
    #         #print(request.url)
    #         pass
    #
    #
    #     playwright = sync_playwright().start()
    #     browser    = playwright.chromium.connect_over_cdp(self.wss_url)
    #
    #     loop = asyncio.get_running_loop()
    #
    #     pprint('[1]' + '-'*100)
    #     pprint(asyncio.all_tasks(loop=loop))
    #     page       = browser.new_page()
    #     page.on("requestfinished", request_finished_handler)
    #
    #     pprint('[2]' + '-' * 100)
    #     pprint(asyncio.all_tasks(loop=loop))
    #     #page.goto('https://www.google.com') # error doesn't happen if this is executed
    #     #page.remove_listener("requestfinished", request_finished_handler)
    #     #page.goto('https://www.google.com')
    #     pprint('[3]' + '-' * 100)
    #     pprint(asyncio.all_tasks(loop=loop))
    #     playwright.stop()












