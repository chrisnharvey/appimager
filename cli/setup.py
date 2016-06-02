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

        for line in docker.pull('nimbusoft/appimager', stream=True):
            print(json.loads(line.decode('utf-8'))['status'])

        volume = os.getcwd() + ':/appimager'

        container_name = data_obj.get_path_hash()

        docker.create_container('nimbusoft/appimager', volumes=volume, command="/bin/bash", name=container_name)
