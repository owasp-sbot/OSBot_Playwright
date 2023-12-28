import pytest
from unittest                               import TestCase
from osbot_docker.apis.Docker_Container     import Docker_Container
from osbot_utils.utils.Misc                 import wait_for
from osbot_utils.utils.Dev                  import pprint
from osbot_utils.utils.Files                import folder_name

from osbot_playwright.docker.Local__Docker_Playwright import Local__Docker_Playwright

#@pytest.mark.skip('while debugging error')
class test_Local__Docker_Playwright(TestCase):

    local_docker : Local__Docker_Playwright

    @classmethod
    def setUpClass(cls) -> None:
        cls.local_docker = Local__Docker_Playwright()
        assert len(cls.local_docker.containers_with_label()) == 0

    @classmethod
    def tearDownClass(cls) -> None:
        cls.local_docker.delete_container()
        assert len(cls.local_docker.containers_with_label()) == 0

    def test___init__(self):
        assert self.local_docker.image_name                      == 'osbot_playwright'
        assert folder_name(self.local_docker.path_images)        == 'images'
        assert type(self.local_docker.create_image_ecr).__name__ == 'Create_Image_ECR'


    def test_create_or_reuse_container(self):
        assert self.local_docker.container                         is None
        assert self.local_docker.create_or_reuse_container()       is True
        assert self.local_docker.container                         is not None
        assert type(self.local_docker.container)                   is Docker_Container
        assert self.local_docker.wait_for_uvicorn_server_running() is True
        container_info = self.local_docker.container.info()
        container_logs = self.local_docker.container.logs()

        assert container_info.get('args'       ) == ['-c', 'exec python3 handler.py']
        assert container_info.get('entrypoint' ) is None
        assert container_info.get('image'      ) == self.local_docker.docker_image.image_name_with_tag()
        #assert container_info.get('ports'      ) == {'8000/tcp': [{'HostIp': '0.0.0.0', 'HostPort': '8888'}]}  # todo: add better supprt for GH action (in there we get [{'HostIp': '0.0.0.0', 'HostPort': '8888'}, {'HostIp': '::', 'HostPort': '8888'}]} )
        assert container_info.get('status'     ) == 'running'
        assert container_info.get('volumes'    ) is None
        assert container_info.get('working_dir') == '/var/task'
        assert container_logs                    == ('INFO:     Started server process [1]\n'
                                                     'INFO:     Waiting for application startup.\n'
                                                     'INFO:     Application startup complete.\n'
                                                     'INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)\n')


    def test_containers_with_label(self):
        containers = self.local_docker.containers_with_label()
        containers = self.local_docker.api_docker.containers_all__by_labels()
        pprint(dict(containers))

    # def test_setup(self):
    #
    #     assert len(self.local_docker.containers_with_label()) == 1
    #
    #     container = self.local_docker.container
    #
    #     assert 'push-docker.sh'           in self.local_docker.container.exec('ls -la .')
    #     assert 'import sys'               in container.exec('cat ./handler.py')
    #     assert self.local_docker.GET('/') == '{"message":"Hello from docked_playwright lambda!!"}'
    #     assert 'GET / HTTP/1.1" 200 OK\n' in container.logs()
    #
    #
    #     pprint(self.local_docker.POST('/lambda-shell'), {})

    def test_z_GET(self):
        assert self.local_docker.GET('/') == '{"message":"Hello from docked_playwright lambda!!!!!"}'

    def test_z_fastapi__root(self):
        assert self.local_docker.GET('/') == '{"message":"Hello from docked_playwright lambda!!!!!"}'





