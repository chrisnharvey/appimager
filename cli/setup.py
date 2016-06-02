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

    @expose(help='Sets up a docker container for building AppImages.')
    def setup(self):
        data_obj = data.Data()
        path = data_obj.get_work_path()

        docker = Client()

        print('Setting up environment, please wait...')

        volume = os.getcwd()

        container_name = data_obj.get_path_hash()

        docker.create_container('nimbusoft/appimager', tty=True, command="/bin/bash", name=container_name, volumes=['/mnt/appimager'],
            host_config=docker.create_host_config(binds={
                os.getcwd(): {
                    'bind': '/mnt/appimager',
                    'mode': 'rw',
                }
            }))

        docker.start(container_name)
        print('Setup Complete')
