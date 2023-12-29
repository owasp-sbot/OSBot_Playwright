import pytest
import platform
import requests
import osbot_playwright
from unittest                                           import TestCase
from osbot_utils.testing.Duration                       import Duration
from osbot_utils.utils.Dev                              import pprint
from osbot_utils.utils.Files                            import folder_exists, folder_name, file_exists, file_name
from osbot_utils.utils.Misc                             import wait_for

from osbot_playwright._extra_methdos_osbot import in_github_actions
from osbot_playwright.docker.Build__Docker_Playwright   import Build__Docker_Playwright


#@pytest.mark.skip('while debugging error')
class test_Build__Docker_Playwright(TestCase):

    def setUp(self) -> None:
        self.build_docker  = Build__Docker_Playwright()
        self.aws_config     = self.build_docker.create_image_ecr.aws_config
        self.aws_account_id = self.aws_config.aws_session_account_id()

    def test__init__(self):
        create_image_ecr  = self.build_docker.create_image_ecr
        deploy_lambda     = self.build_docker.deploy_lambda
        docker_image      = create_image_ecr.docker_image
        docker_image_name = f'{self.aws_account_id}.dkr.ecr.eu-west-2.amazonaws.com/{self.build_docker.image_name}'

        assert self.build_docker.image_name                 == 'osbot_playwright'
        assert self.build_docker.path_images                == create_image_ecr.path_images
        assert type(create_image_ecr             ).__name__ == 'Create_Image_ECR'
        assert type(create_image_ecr.api_docker  ).__name__ == 'API_Docker'
        assert type(create_image_ecr.ecr         ).__name__ == 'ECR'
        assert type(create_image_ecr.docker_image).__name__ == 'Docker_Image'
        assert type(deploy_lambda                ).__name__ == 'Deploy_Lambda'
        assert create_image_ecr.image_name                  == 'osbot_playwright'
        assert create_image_ecr.image_tag                   == 'latest'
        assert create_image_ecr.path_images                 == f'{osbot_playwright.path}/docker/images'
        assert docker_image.api_docker                      == create_image_ecr.api_docker
        assert docker_image.image_id                        == ''
        assert docker_image.image_name                      == docker_image_name
        assert docker_image.image_tag                       == 'latest'

        assert folder_exists(create_image_ecr.path_images) is True

    # def test_aa_pull_image(self):   # todo: see if this really adds value
    #     if in_github_actions():
    #         image_name = f'{self.aws_account_id}.dkr.ecr.eu-west-2.amazonaws.com/{self.build_docker.image_name}:latest'
    #         self.build_docker.create_image_ecr.ecr_login()
    #         result = self.build_docker.create_image_ecr.api_docker.client_docker().images.pull(image_name)
    #         pprint(result)

    def test_build_docker_image(self):
        result = self.build_docker.build_docker_image()
        #pprint(result)
        image  = result.get('image')
        assert result.get('status'      )    == 'ok'
        assert result.get('tags'        )[0] == f'{self.aws_account_id}.dkr.ecr.eu-west-2.amazonaws.com/{self.build_docker.image_name}:latest'
        assert image.get ('Architecture')    == self.build_docker.image_architecture()
        assert image.get ('Os'          )    == 'linux'

    def test_create_container(self):
        container           = self.build_docker.create_container()
        container_id        = container.container_id
        created_containers  = self.build_docker.created_containers()
        assert container.status()       == 'created'
        assert len(created_containers)  == 1
        assert container_id             in created_containers
        assert container.delete()       is True
        assert len(self.build_docker.created_containers().items()) == 0



    def test_image_architecture(self):
        architecture = self.build_docker.image_architecture()

        if platform.system() == 'Darwin':                                                   # Determine the expected architecture based on the platform.
            expected_architecture = 'arm64' if platform.machine() == 'arm64' else 'amd64'   # Mac OS X systems
        else:
            expected_architecture = 'amd64'                                                 # Default to 'amd64' for other systems like GitHub Actions CI
        assert architecture == expected_architecture


    def test_start_container(self):
        assert self.build_docker.build_docker_image().get('status') == 'ok'
        container = self.build_docker.start_container()
        ports     = container.info().get('ports')

        assert container.status() == 'running'
        assert len(ports) == 1
        assert ports.get('8000/tcp')[0].get('HostPort') == '8888'

        with Duration():
            for i in range(0,10):
                if 'Uvicorn running on ' in container.logs():
                    pprint(container.logs())
                    break
                print(f'[{i}] waiting for Uvicorn running on in container logs')
                wait_for(0.1)

        url = "http://localhost:8888"

        response = requests.get(url)
        assert response.status_code == 200
        assert response.text == '{"message":"Hello from docked_playwright lambda!!!!!"}'

        assert container.stop() is True
        assert container.status() == 'exited'
        assert container.delete() is True


    def test_dockerfile(self):
        assert self.build_docker.dockerfile().startswith('FROM mcr.microsoft.com/playwright/python:v1.40.0-jammy')

    def test_path_docker_playwright(self):
        assert folder_exists(self.build_docker.path_docker_playwright()) is True
        assert folder_name  (self.build_docker.path_docker_playwright()) == 'osbot_playwright'

    def test_path_dockerfile(self):
        assert file_exists(self.build_docker.path_dockerfile())
        assert file_name  (self.build_docker.path_dockerfile()) == 'dockerfile'
