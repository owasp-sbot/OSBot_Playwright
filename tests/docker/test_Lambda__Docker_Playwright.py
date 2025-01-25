import os
from unittest import TestCase

import pytest
import requests
from osbot_utils.utils.Env import load_dotenv

from osbot_aws.apis.shell.Lambda_Shell import Lambda_Shell
from osbot_fast_api.utils.http_shell.Http_Shell__Client import Http_Shell__Client
from osbot_utils.testing.Duration import Duration
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import save_bytes_as_file, files_list
from osbot_utils.utils.Functions import function_source_code
from osbot_utils.utils.Json import json_dumps, json_parse, json_loads
from osbot_utils.utils.Misc import bytes_to_base64, base64_to_bytes, list_set

from osbot_playwright._extra_methdos_osbot import in_github_actions
from osbot_playwright.docker.Lambda__Docker_Playwright import Lambda__Docker_Playwright


class test_Lambda__Docker_Playwright(TestCase):
    lambda_docker : Lambda__Docker_Playwright()

    @classmethod
    def setUpClass(cls) -> None:
        cls.lambda_docker = Lambda__Docker_Playwright()
        #cls.lambda_docker.create_lambda_function_url()

    @classmethod
    def tearDownClass(cls) -> None:
        lambda_function = cls.lambda_docker.lambda_function()
        if lambda_function.function_url_exists():
            lambda_function.function_url_delete()

    def setUp(self):
        self.lambda_docker = Lambda__Docker_Playwright()

    def auth_key__shell_server(self):
        load_dotenv()
        return os.environ.get('HTTP_SHELL__AUTH_KEY')

    def test_create_lambda(self):
        delete_existing = True
        wait_for_active = True
        lambda_function = self.lambda_docker.lambda_function()

        if in_github_actions():
            with Duration(prefix='create lambda:'):
                create_result   = self.lambda_docker.create_lambda(delete_existing=delete_existing, wait_for_active=wait_for_active)

                pprint(create_result)

                assert lambda_function.exists() is True
                lambda_info     = lambda_function.info()
                if delete_existing is True:
                    assert create_result.get('create_result').get('status') == 'ok'
                assert lambda_info.get('Configuration').get('State') == 'Active'

        payload     = {'path': '/config/status', 'httpMethod': 'GET'}
        http_status = '{"status":"ok"}'
        with Duration(prefix='invoke lambda 1st:'):
            invoke_result   = lambda_function.invoke(payload)
            assert invoke_result.get('body') == http_status

        with Duration(prefix='invoke lambda 2nd:'):
            invoke_result   = lambda_function.invoke(payload)
            assert invoke_result.get('body') == http_status

        with Duration(prefix='invoke lambda 3rd:'):
            invoke_result   = lambda_function.invoke(payload)
            assert invoke_result.get('body') == http_status

    def test_create_lambda_function_url(self):
        if in_github_actions():
            path_status   = 'config/status'
            http_status  = {"status":"ok"}
            result       = self.lambda_docker.create_lambda_function_url()

            function_url = result.get('FunctionUrl')
            assert result.get('AuthType'   ) == 'NONE'
            assert result.get('FunctionArn') == self.lambda_docker.deploy_lambda.lambda_function().function_arn()
            assert result.get('InvokeMode' ) == 'BUFFERED'
            assert function_url.endswith('.lambda-url.eu-west-2.on.aws/')
            url = function_url + path_status
            assert requests.get(url).json() == http_status

    def test_invoke_lambda_function_url(self):
        if not in_github_actions():
            return  # 'skipping test in local environment'
        path_status   = 'config/status'
        http_status  = {"status":"ok"}
        function_url = self.lambda_docker.lambda_function().function_url()

        #if function_url:
        url = function_url + path_status
        assert requests.get(url).json() == http_status

    def test_invoke_lambda_function_url__shell_server(self):
        if not in_github_actions():
            return # 'skipping test in local environment'
        shell_url    = self.lambda_docker.url_shell_server()
        data         = { "auth_key": self.auth_key__shell_server(),
                         "data"    : { "method_name": "ping",  "method_kwargs": {} } }
        response     = requests.post(shell_url, json=data)
        assert response.json().get('return_value') == 'pong'

    def test_invoke_lambda_function_url__shell_client(self):
        if not in_github_actions():
            return  # 'skipping test in local environment'
        def the_answer(): return 40+2
        shell_url    = self.lambda_docker.url_shell_server()
        shell_client = Http_Shell__Client(shell_url)
        assert shell_client.ping()                    == 'pong'
        assert shell_client.exec_function(the_answer) == 42

    def test_invoke_lambda_function_url__shell_client__get_env_vars(self):
        if not in_github_actions():
            return # 'skipping test in local environment'
        def get_lambda_env_vars():
            return dict(os.environ)

        shell_url       = self.lambda_docker.url_shell_server()
        shell_client    = Http_Shell__Client(shell_url)
        lambda_env_vars = shell_client.exec_function(get_lambda_env_vars)
        vars_names      = list_set(lambda_env_vars)
        assert vars_names == [ 'AWS_ACCESS_KEY_ID', 'AWS_DEFAULT_REGION', 'AWS_EXECUTION_ENV',
                               'AWS_LAMBDA_FUNCTION_MEMORY_SIZE', 'AWS_LAMBDA_FUNCTION_NAME', 'AWS_LAMBDA_FUNCTION_VERSION',
                               'AWS_LAMBDA_INITIALIZATION_TYPE', 'AWS_LAMBDA_LOG_GROUP_NAME', 'AWS_LAMBDA_LOG_STREAM_NAME',
                               'AWS_LAMBDA_RUNTIME_API', 'AWS_REGION', 'AWS_SECRET_ACCESS_KEY', 'AWS_SESSION_TOKEN',
                               'AWS_XRAY_CONTEXT_MISSING', 'AWS_XRAY_DAEMON_ADDRESS', 'HTTP_SHELL__AUTH_KEY',
                               'LAMBDA_RUNTIME_DIR', 'LAMBDA_TASK_ROOT', 'LC_CTYPE', 'PATH',
                               'PLAYWRIGHT_BROWSERS_PATH',  'PORT', 'PWD', '_AWS_XRAY_DAEMON_ADDRESS',
                               '_AWS_XRAY_DAEMON_PORT', '_HANDLER']
        assert lambda_env_vars.get('AWS_EXECUTION_ENV'       ) == 'AWS_Lambda_Image'
        assert lambda_env_vars.get('LAMBDA_RUNTIME_DIR'      ) == '/var/runtime'
        assert lambda_env_vars.get('LAMBDA_TASK_ROOT'        ) == '/var/task'
        assert lambda_env_vars.get('PORT'                    ) == '8000'
        assert lambda_env_vars.get('PWD'                     ) == '/var/task'
        assert lambda_env_vars.get('PLAYWRIGHT_BROWSERS_PATH') == '/ms-playwright'

    # def test_image_architecture(self):
    #     result = self.lambda_docker.create_image_ecr.ecr.client().describe_images(repositoryName='osbot_playwright', imageIds=[{'imageTag': 'latest'}])
    #     #result = self.lambda_docker.create_image_ecr.docker_image.info()
    #     pprint(result)

    def test_execute_lambda(self):
        payload = {'path': '/config/status', 'httpMethod': 'GET'}
        result = self.lambda_docker.execute_lambda(payload)
        assert result.get('body') == '{"status":"ok"}'

    def test_invoke_lambda_function(self):
        with Duration(prefix="Invoking Lambda function"):
            payload = {'path': '/config/status', 'httpMethod': 'GET'}
            lambda_function = self.lambda_docker.lambda_function()
            result = lambda_function.invoke(payload)
            assert result.get('body') == '{"status":"ok"}'

    def test_update_lambda_function(self):
        #pprint(self.build_deploy.lambda_function().info())
        result = self.lambda_docker.update_lambda_function()
        assert result.get('State') == 'Active'


    def test_invoke_fast_api__docs(self):
        payload = {
            "httpMethod": "GET",
            "path": "/docs",
            #"path": "/openapi.json",
            "headers": {
                "Content-Type": "application/json"
            },
            "queryStringParameters": {
                "param1": "value1",
                "param2": "value2"
            },
            "body": "{}"
        }


        result = self.lambda_docker.execute_lambda(payload=payload)
        assert '<title>FastAPI - Swagger UI</title>' in result.get('body')

    def test_invoke_fast_api__shell_server(self):
        load_dotenv()
        auth_key  = os.environ.get('HTTP_SHELL__AUTH_KEY')
        data      = { "auth_key"   : auth_key                                     ,
                      "data"       : { "method_name": "ping", "method_kwargs": {} }}
        payload   = { "httpMethod" : "POST"                                       ,
                      "path"       : "/shell-server"                              ,
                      "headers"    : { "Content-Type": "application/json"        },
                      "body"       : json_dumps(data)                             }
        result      = self.lambda_docker.execute_lambda(payload=payload)
        result_body = json_loads(result.get('body'))
        assert result.get     ('statusCode'  ) == 200
        assert result_body.get('status'      ) == 'ok'
        assert result_body.get('return_value') == 'pong'



    @pytest.mark.skip('see if we need this to start a process in Lambda')
    def test_invoke_fast_api__lambda_shell__starting_process__not_working(self):
        def exec_function(function):
            function_name = function.__name__
            function_code = function_source_code(function)
            exec_code = f"{function_code}\nresult = {function_name}()"
            lambda_shell = Lambda_Shell()
            body = {'method_name': 'python_exec', 'method_kwargs': {'code': exec_code},
                    'auth_key': lambda_shell.get_lambda_shell_auth()}

            payload = {
                "httpMethod": "POST",
                "path": "/lambda-shell",
                # "path": "/openapi.json",
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": json_dumps(body)
            }
            result = self.lambda_docker.execute_lambda(payload=payload)
            return result.get('body')

        def code():
            from osbot_utils.utils.Files import files_list, file_exists, folder_exists
            from osbot_playwright.playwright.api.Playwright_Browser__Chrome import Playwright_Browser__Chrome
            playwright_browser_chrome = Playwright_Browser__Chrome(port=9910)
            # return playwright_browser_chrome.browser_name
            # return playwright_browser_chrome.is_installed()
            playwright_process = playwright_browser_chrome.playwright_process
            #return f"{playwright_process}"
            import os
            os.environ['PLAYWRIGHT_BROWSERS_PATH'] = '/ms-playwright'
            #'PLAYWRIGHT_BROWSERS_PATH': '/ms-playwright',
            browser_path = "/ms-playwright/chromium-1091/chrome-linux/chrome"
            if False:
                #params = [playwright_process.browser_path, f'{CHROMIUM_PARAM_DEBUG_PORT}={playwright_process.debug_port}',
                #          f'{CHROMIUM_PARAM_DATA_FOLDER}={browser_data_folder}']

                #if playwright_process.headless:
                #    params.append(CHROMIUM_PARAM_HEADLESS)
                #params.append('--no-sandbox')
                #params.append("--no-zygote")
                #params.append("--in-process-gpu")
                params= [browser_path, '--remote-debugging-port=9910', "--disable-gpu", "--single-process"]
                from osbot_utils.utils.Files import folder_create
                #folder_create(browser_data_folder)  # make sure folder exists (which in some cases is not created in time to save the process_details)

                import subprocess
                process = subprocess.Popen(params)
                playwright_process.save_process_details(process, playwright_process.debug_port)

            #return file_exists(browser_path)
            from osbot_utils.utils.Http import GET
            #return GET('http://127.0.0.1:9910')
            return playwright_process.healthcheck()
            return playwright_process.process_details()

        result = exec_function(code)
        #pprint(result)
        pprint(json_parse(result))

    @pytest.mark.skip('refactor these "working tests :) into fast api methods')
    def test_invoke_fast_api__lambda_shell(self):
        def exec_function(function):
            function_name = function.__name__
            function_code = function_source_code(function)
            exec_code = f"{function_code}\nresult = {function_name}()"
            lambda_shell = Lambda_Shell()
            body = {'method_name': 'python_exec', 'method_kwargs': {'code': exec_code},
                    'auth_key': lambda_shell.get_lambda_shell_auth()}

            payload = {
                "httpMethod": "POST",
                "path": "/lambda-shell",
                # "path": "/openapi.json",
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": json_dumps(body)
            }
            result = self.lambda_docker.execute_lambda(payload=payload)
            return result.get('body')

        def code():
            #import os
            #return dict(os.environ)
            from playwright.sync_api import sync_playwright
            from osbot_utils.utils.Files import files_list, file_exists, folder_exists
            with sync_playwright() as p:
                browser = p.chromium.launch(args=["--disable-gpu", "--single-process"])
                page = browser.new_page()
                page.goto('https://www.thecyberboardroom.com/')
                return page.content()
                #return f'{}'


        result = exec_function(code)
        pprint(result)
        #pprint(json_parse(result))


    @pytest.mark.skip('refactor these "working tests :) into fast api methods')
    def test_invoke_fast_api__lambda_shell__working_playwright_screenshot(self):
        def code():

            # try:
            #     import asyncio
            #     _loop = asyncio.get_running_loop()
            #     return f'{_loop}'
            # except RuntimeError:
            #     return 'no loop'

            from osbot_playwright.playwright.api.Playwright_Install import Playwright_Install
            #playwright_install = Playwright_Install()


            from osbot_playwright.playwright.api.Playwright_CLI import Playwright_CLI
            playwright_cli = Playwright_CLI()
            #return playwright_cli.install__chrome()
            playwright_cli.set_os_env_for_browsers_path()
            #return playwright_cli.executable_version__chrome() # '"Chromium 120.0.6099.28"'


            from osbot_playwright.playwright.api.Playwright_Browser__Chrome import Playwright_Browser__Chrome
            playwright_browser_chrome = Playwright_Browser__Chrome(port=9910)
            #return playwright_browser_chrome.browser_name
            #return playwright_browser_chrome.is_installed()
            playwright_process = playwright_browser_chrome.playwright_process
            from osbot_utils.utils.Files import files_list
            from osbot_utils.utils.Files import file_contents
            # print('*'*100)
            # import os
            # os.environ['FONTCONFIG_PATH'] = '/opt/fonts'
            # os.environ['DBUS_SESSION_BUS_ADDRESS'] = "/dev/null"
            from playwright.sync_api import sync_playwright

            with sync_playwright() as playwright:
                try:
                    browser = playwright.chromium.launch(args=["--disable-gpu", "--single-process"])
                    #browser = playwright.chromium.launch()
                    new_page = browser.new_page()
                    #new_page.goto('https://www.google.com/404')
                    #new_page.goto('https://news.bbc.co.uk')
                    new_page.goto('https://www.thecyberboardroom.com')
                    #return f'{new_page.content()}'
                    from osbot_utils.utils.Misc import bytes_to_base64
                    return bytes_to_base64(new_page.screenshot(full_page=True))
                except Exception as error:
                    return f'{error}'


            return 'here'
            #return file_contents("/tmp/playwright_chrome_data_folder_in_port__9910/playwright_process.json")
            #return files_list(playwright_process.path_data_folder())

            browser_data_folder = playwright_process.path_data_folder()
            from osbot_playwright.playwright.api.Playwright_Process import CHROMIUM_PARAM_DEBUG_PORT
            from osbot_playwright.playwright.api.Playwright_Process import CHROMIUM_PARAM_DATA_FOLDER
            from osbot_playwright.playwright.api.Playwright_Process import CHROMIUM_PARAM_HEADLESS

            if False:   # this wasking working since the process wasn't holding on
                params = [playwright_process.browser_path, f'{CHROMIUM_PARAM_DEBUG_PORT}={playwright_process.debug_port}',
                          f'{CHROMIUM_PARAM_DATA_FOLDER}={browser_data_folder}']

                if playwright_process.headless:
                    params.append(CHROMIUM_PARAM_HEADLESS)
                params.append('--no-sandbox')
                params.append("--no-zygote")
                params.append("--in-process-gpu")
                from osbot_utils.utils.Files import folder_create
                folder_create(browser_data_folder)  # make sure folder exists (which in some cases is not created in time to save the process_details)

                import subprocess
                process = subprocess.Popen(params)
                playwright_process.save_process_details(process, playwright_process.debug_port)

            return playwright_process.healthcheck()

            #return f'process: {process}'

            #return playwright_browser_chrome.playwright_process.start_process()
            #return playwright_browser_chrome.logger.memory_handler_messages()
            #return playwright_browser_chrome.playwright_process.debug_port
            browser = playwright_browser_chrome.browser()
            return f'browser: {browser}'


            #return playwright_install.browsers_details()

            # from playwright.sync_api import sync_playwright
            # with sync_playwright() as playwright:
            #     browser = playwright.chromium.launch()
            #     page    = browser.new_page()
            #     url = page.url
            #     #page.goto('http://whatsmyuseragent.org/')
            #     #page.screenshot(path='example.png')
            #     browser.close()
            #     return url
            #return f"Playwright: {sync_playwright}"
            #

            #answer = 40 + 2123
            #return answer

        function_name = code.__name__
        function_code = function_source_code(code)
        exec_code     = f"{function_code}\nresult = {function_name}()"
        lambda_shell = Lambda_Shell()
        body={'method_name': 'python_exec', 'method_kwargs': {'code': exec_code},
              'auth_key': lambda_shell.get_lambda_shell_auth()}

        payload = {
            "httpMethod": "POST",
            "path": "/lambda-shell",
            #"path": "/openapi.json",
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json_dumps(body)
        }


        result = self.lambda_docker.execute_lambda(payload=payload)
        body = result.get('body')
        bytes =  base64_to_bytes(body)
        print(save_bytes_as_file (bytes, '/tmp/screenshot.png'))
        #pprint(json_parse(body))
        #pprint(body)
        #print(bytes)

    #def test_invoke_lambda_shell(self):

        # aws_lambda = self.lambda_docker.lambda_function()
        # from osbot_aws.apis.shell.Shell_Client import Shell_Client
        # lambda_client = Shell_Client(aws_lambda)
        #
        # pprint(lambda_client.ping())

    # def test_z_aws_publish(self):
    #     #build_result = self.build_docker.build_docker_image()       # make sure the image is built
    #     #assert build_result.get('status') == 'ok'
    #
    #     result          = self.lambda_docker.create_image_ecr.push_image()
    #     auth_result     = result.get('auth_result')
    #     push_json_lines = result.get('push_json_lines')
    #     assert auth_result.get('Status') ==     'Login Succeeded'
    #     assert 'errorDetail'             not in push_json_lines