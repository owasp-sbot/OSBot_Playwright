import pytest
from unittest import TestCase

from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import folder_name

from osbot_playwright.docker.Local__Docker_Playwright import Local__Docker_Playwright

@pytest.mark.skip("to wrire up")
class test_Local__Docker_Playwright(TestCase):

    local_docker : Local__Docker_Playwright

    @classmethod
    def setUpClass(cls) -> None:
        cls.local_docker = Local__Docker_Playwright()
        assert len(cls.local_docker.containers_with_label()) == 0
        #cls.local_docker.setup()

    @classmethod
    def tearDownClass(cls) -> None:
        assert cls.local_docker.delete_container()           is False
        assert len(cls.local_docker.containers_with_label()) == 0

    def test___init__(self):
        assert self.local_docker.image_name                      == 'osbot_playwright'
        assert folder_name(self.local_docker.path_images)        == 'images'
        assert type(self.local_docker.create_image_ecr).__name__ == 'Create_Image_ECR'


    def test_containers_with_label(self):
        containers = self.local_docker.containers_with_label()
        containers = self.local_docker.api_docker.containers_all__by_labels()
        pprint(dict(containers))

    def test_setup(self):

        assert len(self.local_docker.containers_with_label()) == 1

        container = self.local_docker.container

        assert 'push-docker.sh'           in self.local_docker.container.exec('ls -la .')
        assert 'import sys'               in container.exec('cat ./handler.py')
        assert self.local_docker.GET('/') == '{"message":"Hello from docked_playwright lambda!!"}'
        assert 'GET / HTTP/1.1" 200 OK\n' in container.logs()


        pprint(self.local_docker.POST('/lambda-shell'), {})

    def test_GET(self):
        assert self.local_docker.GET('/') == '{"message":"Hello from docked_playwright lambda!!"}'

    def test_fastapi__root(self):
        assert self.local_docker.GET('/') == '{"message":"Hello from docked_playwright lambda!!"}'





