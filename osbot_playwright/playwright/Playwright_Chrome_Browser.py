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
    def browser_connect_over_cdp(self):
        browser_url = self.url_browser_debug_page()
        chromium = self.chromium()
        return chromium.connect_over_cdp(endpoint_url=browser_url)

    def browser_connect_to_existing_process(self):
        if self.process_running() is False:
            self.logger.error("No existing process found to connect to")
            return False
        self.logger.info("Connecting to existing Chromium process")
        try:
            self._browser = self.browser_connect_over_cdp()
            if self._browser:
                self.logger.info(f"Connected ok to Chromium version : { self._browser.version }")
                return True
        except Exception as error:
            self.logger.error(f"[Playwright_Chrome] in browser_connect: {error}")
        return False

    def chromium(self):
        return self.playwright().chromium

    def chromium_exe_path(self):
        return self.chromium().executable_path

    def close_all_context_and_pages(self):
        contexts_closed  = 0
        pages_closed = 0
        contexts = self.contexts() or []
        for context in contexts:
            for page in context.pages:
                self.logger.info(f"Closing page: {page}")
                self.close_page(page)
                #page.close()
                pages_closed += 1
            try:
                self.close_context(context)
            except Error:      # for the cases where the context has already been closed
                continue
            contexts_closed += 1
        self.logger.info(f"Closed {pages_closed} pages and {contexts_closed} contexts")

    def close_context(self, context):
        context.close()

    def close_page(self, page):
        page.close()

    def config(self):
        return dict(debug_port                   = self.debug_port        ,
                    path_data_folder             = self.path_data_folder(),
                    path_file_playwright_process = self.path_file_playwright_process())

    def contexts(self):
        if self.browser():
            return self.browser().contexts
        return []


    def context(self, index=0):
        contexts = self.contexts()
        if contexts and len(contexts) > index:
            return contexts[index]

    def delete_process_details(self):
        return file_delete(self.path_file_playwright_process())

    def delete_browser_data_folder(self):
        browser_data_folder = self.path_data_folder()
        assert temp_folder_current() in browser_data_folder         # always double check that we are going to delete recursively in the right location
        folder_delete_recursively(browser_data_folder)

    def healthcheck(self):
        config                         = self.config()
        data_folder_exists             = folder_exists(config.get('path_data_folder'))
        playwright_process_file_exists = file_exists(config.get('path_file_playwright_process'))
        process_details                = self.process_details()


        if process_details == {}:
            chromium_debug_port     = None
            chromium_process_id     = None
            chromium_process_exists = False
            chromium_process_status = None
        else:
            chromium_debug_port     = process_details.get('debug_port')
            chromium_process_id     = process_details.get('process_id')
            chromium_process_exists = True
            chromium_process_status = process_details.get('status'    )

        chromium_debug_port_match   = chromium_debug_port == self.debug_port
        if chromium_debug_port and chromium_debug_port_match:
            chromium_debug_port_open = port_is_open(chromium_debug_port)
        else:
            chromium_debug_port_open = False

        if (chromium_process_status =='running' or chromium_process_status=='sleeping') \
                and chromium_debug_port_match                                           \
                and chromium_debug_port_open                                            \
                and chromium_process_exists                                             \
                and data_folder_exists:
            healthy = True
        else:
            healthy = False
        return dict(chromium_debug_port            = chromium_debug_port            ,
                    chromium_debug_port_match      = chromium_debug_port_match      ,
                    chromium_debug_port_open       = chromium_debug_port_open       ,
                    chromium_process_id            = chromium_process_id            ,
                    chromium_process_exists        = chromium_process_exists        ,
                    chromium_process_status        = chromium_process_status        ,
                    data_folder_exists             = data_folder_exists             ,
                    healthy                        = healthy                        ,
                    playwright_process_file_exists = playwright_process_file_exists )

    def healthy(self):
        return self.healthcheck().get('healthy')

    def load_process_details(self):
        return json_load_file(self.path_file_playwright_process())

    def new_page(self, context_index=0):
        context = self.context(index=context_index)
        if context:
            page = context.new_page()
            return Playwright_Page(context=context, page=page)

    def pages(self, context_index=0):
        pages = []
        context = self.context(index=context_index)
        if context:
            for page in context.pages:
                pages.append(Playwright_Page(context=context, page=page))
        return pages

    def page(self, context_index=0, page_index=0):
        pages = self.pages(context_index=context_index)
        if pages and len(pages) > page_index:
            return pages[page_index]

    def path_data_folder(self):
        data_folder_name = FORMAT_CHROME_DATA_FOLDER.format(port=self.debug_port)
        path_data_folder = path_combine(temp_folder_current(), data_folder_name)
        return path_data_folder

    def path_file_playwright_process(self):
        return path_combine(self.path_data_folder(), FILE_PLAYWRIGHT_PROCESS)
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

    def process_id(self):
        return self.process_details().get('process_id')

        #healthcheck = self.healthcheck()
        #if healthcheck.get('healthy') is True:
        #    return healthcheck.get('chromium_process_id')

    def process_details(self):
        process_details = self.load_process_details()
        process_id            = process_details.get('process_id')
        if process_id:
            try:
                process = psutil.Process(process_id)
                process_details['status'] = process.status()                # add the status to the data loaded from disk
                return process_details
            except psutil.NoSuchProcess:
                pass
        return {}

    def process_status(self):
        return self.process_details().get('status')

    def process_running(self):
        return self.process_id() is not None

    def start_process(self):
        if self.process_running():
            self.logger.error("There is already an chromium process running")
            return False

        chromium_path       = self.chromium_exe_path()
        browser_data_folder = self.path_data_folder()
        params = [chromium_path, f'{CHROMIUM_PARAM_DEBUG_PORT}={self.debug_port}'      ,
                                 f'{CHROMIUM_PARAM_DATA_FOLDER}={browser_data_folder}' ]

        if self.headless:
            params.append(CHROMIUM_PARAM_HEADLESS)

        folder_create(browser_data_folder)                          # make sure folder exists (which in some cases is not created in time to save the process_details)

        process = subprocess.Popen(params)
        self.save_process_details(process, self.debug_port)

        if self.wait_for_debug_port() is False: #port_is_open(self.chrome_port) is False:
            raise Exception(f"in browser_start_process, port {self.debug_port} was not open after process start")

        self.logger.info(f"started process id {process.pid} with debug port {self.debug_port}")

        self.browser_connect_to_existing_process()

        return True

    def save_process_details(self, process, debug_port):
        data = {
                 'created_at'   : date_now()        ,
                 'debug_port'   : debug_port        ,
                 'headless'     : self.headless     ,
                 'process_args' : process.args      ,
                 'process_id'   : process.pid       ,
                'reuse_browser' : self.reuse_browser
                }
        json_save_file(data, self.path_file_playwright_process())
        return self

    def setup(self):
        if self.process_running() is False:
            self.start_process()
        else:
            self.browser_connect_to_existing_process()
        return self.healthy()

    def stop_process(self):
        if self.process_running():
            process_id = self.process_id()
            if process_id:
                self.logger.info(f"Stopping Chromium process {process_id}")
                self.close_all_context_and_pages()
                stop_process(process_id)

                if wait_for_port_closed(TARGET_HOST, self.debug_port):
                    self.logger.info(f"Port {self.debug_port} is now closed")
                self.delete_process_details()
                self.logger.info(f"Chromium process {process_id} stopped and port {self.debug_port} is closed")
                return True
        return False

    def url_browser_debug_page(self, path=""):
        return f"http://{TARGET_HOST}:{self.debug_port}/{path}"

    def url_browser_debug_page_json(self, path="json"):
        return self.url_browser_debug_page(path)

    def url_browser_debug_page_json_version(self, path="json/version"):
        return self.url_browser_debug_page(path)

    def restart_process(self):
        self.stop_process()
        self.setup()

    def wait_for_debug_port(self):
        return wait_for_port(TARGET_HOST, self.debug_port, max_attempts=50)
