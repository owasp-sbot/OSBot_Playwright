import os
import platform

from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import current_temp_folder, path_combine, folder_exists
from osbot_utils.utils.Process import exec_process


FOLDER_NAME_PLAYWRIGHT_BROWSERS = "osbot_playwright_browsers"
VERSION_PLAYWRIGHT              = "Version 1.49.1"

class Playwright_CLI:

    def __init__(self, use_evn_var_for_browsers_path=True):
        self.use_evn_var_for_browsers_path = use_evn_var_for_browsers_path
        pass

    def __enter__(self): return self
    def __exit__(self, exc_type, exc_val, exc_tb): pass


    def browser_installed(self, browser_name):
        browser_path = self.install_details(browser_name).get('install_location')
        return folder_exists(browser_path)

    def browser_installed__chrome(self):
        return self.browser_installed('chromium')

    def current_os(self):
        os_name = platform.system()
        if os_name == 'Darwin':
            return 'macOS'
        elif os_name == 'Windows':
            return 'Windows'
        elif os_name == 'Linux':
            return 'Linux'
        else:
            return 'Unknown'

    def executable_path__chrome(self):
        install_location = self.install_location('chromium')
        if self.current_os() == 'macOS':
            return path_combine(install_location, 'chrome-mac/Chromium.app/Contents/MacOS/Chromium')
        elif self.current_os() == 'Linux':
            return path_combine(install_location,"chrome-linux/chrome" )  # todo, confirm this

    def executable_version__chrome(self):
        return exec_process(self.executable_path__chrome(), ['--version']).get('stdout').strip()


    def dry_run(self):
        os.environ['PLAYWRIGHT_BROWSERS_PATH'] = '/temp_dir'
        return self.invoke_raw(['install','--dry-run'])

    def help(self):
        return self.invoke_raw('help').get('stdout')

    def invoke_raw(self, params=None):
        return exec_process('playwright', params)

    def install(self, browser_name):
        #self.set_os_env_for_browsers_path()
        browser_path = self.install_details(browser_name).get('install_location')       # get browser installation details
        if folder_exists(browser_path):                                                 # if browser is already installed
            return True                                                                 # just return

        print(f"Browser {browser_name} not installed, installing it now")               # todo: add better logging support
        result = self.invoke_raw(['install', browser_name])                             # install browser via playwright cli install
        print(result)
        return self.browser_installed(browser_name)                                     # return confirmation that the browsers is installed


    def install__chrome(self):
        return self.install('chromium')

    def install_details(self, browser_name):
        self.set_os_env_for_browsers_path()
        params          = ['install', browser_name, '--dry-run']
        stdout          = self.invoke_raw(params).get('stdout')
        parsed_output   = self.parse_stdout__dryrun(stdout)
        return parsed_output.get(browser_name)

    def install_details__chrome(self):
        return self.install_details('chromium')

    def install_location(self, browser_name):
        return self.install_details(browser_name).get('install_location')

    def path_browsers(self):
        return path_combine(current_temp_folder(), FOLDER_NAME_PLAYWRIGHT_BROWSERS)

    #def parse_stdout__dryrun(self, stdout):
        # lines = stdout.strip().split('\n')
        # data  = {}                                                          # Define a dictionary to hold the parsed data
        # for line in lines:                                                  # Iterate over each line
        #     key_value = line.split(':', 1)                                  # Split the line by ':' to separate the key and value
        #     if len(key_value) == 2:                                         # Check if the line contains a key-value pair
        #         key       = key_value[0].strip().replace(' ', '_').lower()    # Clean up the key and value by stripping whitespace
        #         value     = key_value[1].strip()
        #         data[key] = value                                                 # Add the key-value pair to the dictionary
        # return data
    def parse_stdout__dryrun(self, stdout):
        lines = stdout.strip().split('\n')
        data = {}                                                                           # Dictionary to store parsed data
        current_browser = None                                                              # Track the current browser context

        for line in lines:
            if not line.strip():                                                            # Skip empty lines
                continue

            if not line.startswith(' '):                                                    # New browser section
                key_value = line.split(':', 1)
                if len(key_value) == 2:
                    browser_info    = key_value[1].strip()                                     # Extract browser name and version
                    parts           = browser_info.split(" version ", 1)
                    browser_name    = parts[0].strip().lower()
                    browser_version = parts[1].strip() if len(parts) > 1 else None
                    if browser_name not in data:                                            # Initialize the browser entry if not already present
                        data[browser_name] = {}
                    if browser_version:                                                     # Add the version to the browser data
                        data[browser_name]['version'] = browser_version
                    current_browser = browser_name                                          # Set the current browser context
            elif current_browser:                                                           # Add details to the current browser
                key_value = line.split(':', 1)
                if len(key_value) == 2:
                    key   = key_value[0].strip().replace(' ', '_').lower()
                    value = key_value[1].strip()
                    data[current_browser][key] = value
        return data

    def set_os_env_for_browsers_path(self):
        if self.use_evn_var_for_browsers_path:
            os.environ['PLAYWRIGHT_BROWSERS_PATH'] = self.path_browsers()

    def version(self):
        return self.invoke_raw('-V').get('stdout').strip()