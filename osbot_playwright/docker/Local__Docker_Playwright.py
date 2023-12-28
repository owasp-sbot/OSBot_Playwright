from pprint import pformat
import requests
from osbot_aws.helpers.Create_Image_ECR import Create_Image_ECR

from osbot_utils.utils.Files import parent_folder, path_combine
from osbot_utils.utils.Misc import wait_for

import osbot_playwright


class Local__Docker_Playwright:

    def __init__(self):
        self.image_name       = 'osbot_playwright'
        self.path_images      = path_combine(osbot_playwright.path, 'docker/images')
        self.create_image_ecr = Create_Image_ECR(image_name=self.image_name, path_images=self.path_images)
        self.docker_image     = self.create_image_ecr.docker_image
        self.api_docker       = self.create_image_ecr.api_docker
        self.label_source     = 'local__docker_playwright'
        self.labels           = {'source': self.label_source}
        #self.volume_path      = path_combine(self.path_images, 'osbot_playwright')
        self.local_port       = 8888
        self.port_bindings    = {8000: self.local_port }
        # self.volumes          = { self.volume_path: { 'bind': '/var/task',
        #                                               'mode': 'ro'       }}
        self.container        = None

    def create_or_reuse_container(self):
        containers = self.containers_with_label()
        if len(containers) > 0:                                         # if we have one, return it
            return next(iter(containers.values()))

        kwargs = { 'labels'        : self.labels        ,               # if not create one with the correct label
                   #'volumes'       : self.volumes       ,
                   'port_bindings' : self.port_bindings }
        self.container = self.docker_image.create_container(**kwargs)
        return  self.container.start()

    def containers_with_label(self):
        by_labels  = self.api_docker.containers_all__by_labels()
        containers = by_labels.get('source', {}).get(self.label_source, {})
        return containers

    def delete_container(self):
        if self.container:
            self.container.stop()
            return self.container.delete()
        return False

    def GET(self, path=''):
        url = self.local_url(path)
        return requests.get(url).text

    def POST(self, path='', data=None):
        url     = self.local_url(path)
        headers = { 'Content-Type': 'application/json'}
        return requests.post(url, data=data, headers=headers).text

    def local_url(self, path):
        if path.startswith('/') is False:
            path = f'/{path}'
        local_url = f'http://localhost:{self.local_port}{path}'
        return local_url

    def uvicorn_server_running(self):
        return 'Uvicorn running on ' in self.container.logs()

    def wait_for_uvicorn_server_running(self, max_count=40, delay=0.5):
        if self.container is None:
            print(f'[wait_for_uvicorn_server_running] Error: no container running)')
            return False
        for i in range(max_count):
            status = self.container.status()
            if status!= 'running':
                print(f'[wait_for_uvicorn_server_running] Error: container is not runnnng, it is with the state: {status}')
                return False
            if self.uvicorn_server_running():
                return True
            #print(f'[wait_for_uvicorn_server_running] waiting for uvicorn_server to start (attempt {i})')
            wait_for(delay)
        return False




