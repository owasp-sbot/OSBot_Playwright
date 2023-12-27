import asyncio
import subprocess

import psutil
from osbot_utils.decorators.lists.index_by import index_by
from osbot_utils.decorators.methods.cache_on_function import cache_on_function
from osbot_utils.decorators.methods.cache_on_self import cache_on_self
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import temp_folder_current, path_combine, folder_exists, file_exists, file_delete, \
    folder_delete_recursively, folder_create
from osbot_utils.utils.Http import wait_for_port, is_port_open, port_is_open, wait_for_port_closed
from osbot_utils.utils.Json import json_save, json_parse, json_dump, json_load_file, json_save_file
from osbot_utils.utils.Misc import to_int, wait_for, date_now
from osbot_utils.utils.Process import stop_process
from osbot_utils.utils.Python_Logger import logger_error, Python_Logger
from playwright.sync_api import sync_playwright, Error

from osbot_playwright.playwright.Playwright_Page import Playwright_Page

DEFAULT_VALUE_DEBUG_PORT   = 9910
FORMAT_CHROME_DATA_FOLDER  = 'playwright_chrome_data_folder_in_port__{port}'
TARGET_HOST                = 'localhost'
FILE_PLAYWRIGHT_PROCESS    = 'playwright_process.json'
CHROMIUM_PROCESS_NAME      = 'Chromium'
CHROMIUM_PARAM_DEBUG_PORT  = "--remote-debugging-port"
CHROMIUM_PARAM_DATA_FOLDER = "--user-data-dir"
CHROMIUM_PARAM_HEADLESS    = "--headless"


# todo: refactor this class to use API_Playwright
class Playwright_Chrome_Browser:

    def __init__(self, headless=True, reuse_browser=True, debug_port=DEFAULT_VALUE_DEBUG_PORT):
        self.logger        = Python_Logger().setup()
        self.headless      = headless
        self.reuse_browser = reuse_browser
        self.debug_port    = debug_port
        self._browser      = None

    def __enter__(self): return self
    def __exit__(self, exc_type, exc_val, exc_tb): return False

    def browser(self):
        return self._browser

    # this is a weird one, since code coverage was breaking with the chromium.connect_over_cdp call
    # def browser_connect_over_cdp(self):
    #     browser_url = self.url_browser_debug_page()
    #     chromium = self.chromium()
    #     return chromium.connect_over_cdp(endpoint_url=browser_url)
    #
    # def browser_connect_to_existing_process(self):
    #     if self.process_running() is False:
    #         self.logger.error("No existing process found to connect to")
    #         return False
    #     self.logger.info("Connecting to existing Chromium process")
    #     try:
    #         self._browser = self.browser_connect_over_cdp()
    #         if self._browser:
    #             self.logger.info(f"Connected ok to Chromium version : { self._browser.version }")
    #             return True
    #     except Exception as error:
    #         self.logger.error(f"[Playwright_Chrome] in browser_connect: {error}")
    #     return False




    #def safe_state(self):

    # caching on the function object,  makes it so that we don't start another event loop
    # if this is still an issue, one way to go around it is to create a separate class that will hold the playwright object as a singleton
    @cache_on_function
    def playwright(self):
        # if asyncio.get_event_loop().is_running():
        #     raise Exception("Cannot create playwright instance while asyncio event loop is running")
        return sync_playwright().start()

    # def process(self):
    #     return self._process


        #healthcheck = self.healthcheck()
        #if healthcheck.get('healthy') is True:
        #    return healthcheck.get('chromium_process_id')


    def setup(self):
        if self.process_running() is False:
            self.start_process()
        else:
            self.browser_connect_to_existing_process()
        return self.healthy()







