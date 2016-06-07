from cli import base
from core import data
from docker import Client
from cement.core.controller import CementBaseController, expose
import json
import os

class SetupController(CementBaseController):
    class Meta:
        label = 'setup'
        stacked_on = 'base'

    @expose(help='Sets up a Docker container for this environment.')
    def setup(self):
        data_obj = data.Data()
        path = data_obj.get_work_path()
        yml = data_obj.get_yml_data()

        docker = Client()

        print('Setting up environment, please wait...')

        volume = os.getcwd()

        base_os_version = yml['base']
        container_name = data_obj.get_path_hash()

        print('Pulling Ubuntu ' + str(base_os_version) + '...')
        docker.pull('ubuntu', str(base_os_version))

        print('Creating container...')
        docker.create_container('ubuntu:' + str(base_os_version), tty=True, command="/bin/bash", name=container_name, volumes=['/mnt/appimager'],
            host_config=docker.create_host_config(binds={
                os.getcwd(): {
                    'bind': '/mnt/appimager',
                    'mode': 'rw',
                }
            }))

        print('Starting container...')
        docker.start(container_name)

        print('Installing build dependencies...')

        print('Setup Complete')
