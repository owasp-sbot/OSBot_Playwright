from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import file_exists, folder_exists, path_combine, folder_create
from osbot_utils.utils.Json import json_file_load, json_save_file, json_load_file
from playwright.sync_api import sync_playwright

from osbot_playwright.playwright.api.Playwright_CLI import Playwright_CLI

SUPORTTED_BROWSERS        = ['chromium', 'firefox', 'webkit']
FILE_NAME_BROWSER_DETAILS = 'browsers_details.json'

# todo: handle better the case when the browser is updated and the FILE_NAME_BROWSER_DETAILS is out of date
class Playwright_Install:

    def __init__(self):
        self.playwrtight_cli = Playwright_CLI()
        self.playwrtight_cli.set_os_env_for_browsers_path()


    def browser_details(self, browser_name):
        return self.browsers_details().get(browser_name)

    def browsers_details(self, reset_data=False):                       # Define a method that retrieves browser details, with an option to reset data.
        path_browsers_details = self.path_browsers_details()            # Get the path where browser details are stored.
        browsers_details = json_load_file(path_browsers_details)        # Load browser details from a JSON file at the specified path.

        if browsers_details and reset_data is False:                    # Check if browser details exist and reset_data is not requested.
            return browsers_details                                     # Return the existing browser details without modifying.

        browsers_details = self.browsers_details_content()              # Get the content for browser details, potentially by generating them.
        folder_create(self.path_browsers())                             # Ensure the folder for storing browser details exists, create if not.
        json_save_file(browsers_details, path_browsers_details)         # Save the new or updated browser details to the JSON file.
        return browsers_details                                         # Return the new or updated browser details.

    def browsers_details_content(self):
        browsers_details = {}
        executable_paths = self.browsers_executable_paths()
        for browser_name in SUPORTTED_BROWSERS:
            install_details = self.playwrtight_cli.install_details(browser_name)
            installed       = folder_exists(install_details.get('install_location'))
            browser_details = { 'download_url'     : install_details.get('download_url'    ) ,
                                'executable_path'  : executable_paths.get(browser_name     ) ,
                                'install_location' : install_details.get('install_location') ,
                                'installed'        : installed                               ,
                                'version'          : install_details.get('browser'         ) }
            browsers_details[browser_name] = browser_details
        return browsers_details

    def browsers_executable_paths(self):
        executable_paths = {}
        with sync_playwright() as playwright:
            for browser_name in SUPORTTED_BROWSERS:
                executable_paths[browser_name] = playwright.__getattribute__(browser_name).executable_path
        return executable_paths


    def path_browsers(self):
        return self.playwrtight_cli.path_browsers()

    def path_browsers_details(self):
        return path_combine(self.path_browsers(), FILE_NAME_BROWSER_DETAILS)