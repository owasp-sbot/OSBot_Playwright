from unittest import TestCase
from unittest.mock import patch

import requests
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import temp_folder_current, folder_exists, file_exists, files_list, files_names, \
    folders_names
from osbot_utils.utils.Json import json_load_file
from osbot_utils.utils.Misc import list_set, random_port
from osbot_utils.utils.Python_Logger import Python_Logger

from osbot_playwright.playwright.Playwright_Browser__Chrome import Playwright_Browser__Chrome
from osbot_playwright.playwright.Playwright_Process import Playwright_Process, FILE_PLAYWRIGHT_PROCESS, \
    FORMAT_CHROME_DATA_FOLDER, DEFAULT_VALUE_DEBUG_PORT


class test_Playwright_Process(TestCase):
    debug_port         : int
    browser_path       : str
    headless           : bool
    playwright_process : Playwright_Process

    @classmethod
    def setUpClass(cls) -> None:
        cls.debug_port   = random_port()
        cls.browser_path = Playwright_Browser__Chrome().browser_exec_path
        cls.headless = True
        with Playwright_Process(browser_path=cls.browser_path, headless=cls.headless, debug_port=cls.debug_port) as _:
            _.delete_browser_data_folder()
            _.start_process()
            assert _.process_running() is True
            assert folder_exists(_.path_data_folder()) is True
            assert file_exists(_.path_file_playwright_process()) is True
            #assert _.setup() == True
            cls.playwright_process = _

    @classmethod
    def tearDownClass(cls) -> None:
        with cls.playwright_process as _:
            assert _.stop_process()               is True
            #assert _.delete_browser_data_folder() is True

    # def setUp(self):
    #     self.playwright_process = Playwright_Process()

    def test__init__(self):
        print('in Test__init__')
        with self.playwright_process as _:
            assert type(_.logger)    == Python_Logger
            assert _.browser_path    == self.browser_path
            assert _.debug_port      == self.debug_port
            assert _.debug_port      != DEFAULT_VALUE_DEBUG_PORT
            assert _.debug_port      > 19999
            assert _.headless        is True
            assert _.reuse_browser   is True

    def test_config(self):
        config = self.playwright_process.config()
        assert config == { 'debug_port'                  : self.debug_port,
                           'path_data_folder'            : f'{temp_folder_current()}/{FORMAT_CHROME_DATA_FOLDER.format(port=self.playwright_process.debug_port)}',
                           'path_file_playwright_process': f'{temp_folder_current()}/{FORMAT_CHROME_DATA_FOLDER.format(port=self.playwright_process.debug_port)}/{FILE_PLAYWRIGHT_PROCESS}'}

    def test_healthcheck(self):
        with self.playwright_process as _:
            process_id  = _.process_id()
            debug_port  = _.debug_port
            healthcheck = _.healthcheck()

            chromium_process_status = healthcheck.get('chromium_process_status')
            assert chromium_process_status == 'running' or chromium_process_status== 'sleeping'
            del healthcheck['chromium_process_status']

            assert healthcheck == {   'chromium_debug_port'           : debug_port ,
                                      'chromium_debug_port_match'     : True       ,
                                      'chromium_debug_port_open'      : True       ,
                                      'chromium_process_exists'       : True       ,
                                      'chromium_process_id'           : process_id ,
                                      'data_folder_exists'            : True       ,
                                      'healthy'                       : True       ,
                                      'playwright_process_file_exists': True       }
            assert healthcheck.get('chromium_debug_port') == _.debug_port
            assert healthcheck.get('healthy'            ) is True

            with patch.object(_, 'process_details', return_value={}):
                assert _.healthcheck() == { 'chromium_debug_port'           : None  ,
                                            'chromium_debug_port_match'     : False ,
                                            'chromium_debug_port_open'      : False ,
                                            'chromium_process_exists'       : False ,
                                            'chromium_process_id'           : None  ,
                                            'chromium_process_status'       : None  ,
                                            'data_folder_exists'            : True  ,
                                            'healthy'                       : False ,
                                            'playwright_process_file_exists': True  }

    def test_path_data_folder(self):
        data_folder = self.playwright_process.path_data_folder()
        assert folder_exists(data_folder) is True
        assert 'playwright_process.json' in files_names(files_list(data_folder))

    def test_path_file_playwright_process(self):
        path_file_playwright_process = self.playwright_process.path_file_playwright_process()
        assert file_exists(path_file_playwright_process) is True
        assert list_set(json_load_file(path_file_playwright_process)) == ['created_at'  , 'debug_port', 'headless'     ,
                                                                          'process_args', 'process_id', 'reuse_browser']

    def test_process_details(self):
        process_details = self.playwright_process.process_details()
        assert list_set(process_details) == ['created_at'  , 'debug_port', 'headless'     ,
                                             'process_args', 'process_id', 'reuse_browser', 'status','url']


    def test_start_process(self):

        #assert file_exists(browser_path) is True
        path_file_playwright_process = self.playwright_process.path_file_playwright_process()
        with self.playwright_process as _:
            #_.browser_path = browser_path
            assert _.process_running()                       is True              # there should be an existing process
            assert _.healthy()                               is True
            assert _.start_process()                         is False             # confirm we get a False value when the process is already running
            assert file_exists(path_file_playwright_process) is True              # before delete config file should exist

            assert _.stop_process()                          is True              # confirm we can stop the process

            assert _.process_running()                       is False
            assert _.healthy()                               is False
            assert file_exists(path_file_playwright_process) is False             # after delete config file should NOT exist
            assert _.process_details()                       == {}                # confirm that process_details is empty

            assert _.start_process()   is True              # confirm we can start the process again

            assert _.process_running()                       is True
            assert _.healthy()                               is True
            assert file_exists(path_file_playwright_process) is True              # after start config file should exist
            # add tests for started process

            assert list_set(_.version()) == ['Browser', 'Protocol-Version', 'User-Agent',
                                             'V8-Version', 'WebKit-Version', 'webSocketDebuggerUrl']

            # with pytest.raises(Exception) as exc_info:
            #     with patch.object(_, 'wait_for_debug_port', return_value=False):
            #         _.start_process()
            # assert str(exc_info.value) == f'in browser_start_process, port {_.debug_port} was not open after process start'
            #
            # assert _.stop_process() is True



