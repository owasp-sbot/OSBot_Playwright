import os

from osbot_aws.helpers.Create_Image_ECR import Create_Image_ECR
from osbot_utils.utils.Files import path_combine, file_exists, file_contents, file_delete, file_not_exists
from osbot_utils.utils.Json import json_file_load

import osbot_playwright


class ECR__Docker_Playwright:

    def __init__(self):                                     # todo: refactor this init code to a base class that can be shared by the other Docker_Playwright classes
        self.image_name       = 'osbot_playwright'
        self.path_images      = path_combine(osbot_playwright.path, 'docker/images')
        self.create_image_ecr =  Create_Image_ECR(image_name=self.image_name, path_images=self.path_images)

    def ecr_setup(self):
        return self.create_image_ecr.create_repository()

    def publish_docker_image(self):
        if self.check_for_docker_config_json():
            print('Docker config json not found, executing self.create_image_ecr.push_image()')
            return self.create_image_ecr.push_image()
        print('Docker config json found, skipping publish_docker_image')
        return self.create_image_ecr.push_image()

    def check_for_docker_config_json(self):              # todo: move this to OSBOT_Lambda code
        expected_docker_config = {'credsStore': 'desktop'}
        docker_config_json = path_combine(os.environ.get('HOME'), '.docker/config.json')
        if file_exists(docker_config_json):
            docker_config = json_file_load(docker_config_json)
            if docker_config == expected_docker_config:
                print()
                print('#' * 125)
                print(f'## Warning: found the {docker_config_json} with content {expected_docker_config}')
                print(f'##          this causes an known issue with Docker python api, where it is not possible to login to docker hosts like ecr')
                print(f'##          since this file is currently empty, it is going to be deleted')
                print('#' * 125)
                file_delete(docker_config_json)
        return file_not_exists(docker_config_json)



