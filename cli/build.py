import os
from docker import Client
from core import data
from cement.core.controller import CementBaseController, expose

class BuildController(CementBaseController):
    class Meta:
        label = 'build'
        stacked_on = 'base'

    @expose(help='Run the build command/script to compile your application.')
    def build(self):
        data_obj = data.Data()
        container_name = data_obj.get_path_hash()
        yml_data = data_obj.get_yml_data()

        docker = Client()

        cmd = docker.exec_create(container_name, 'sh -c "cd /mnt/appimager && ' + yml_data['build'] + '"')
        cmd_id = cmd['Id']

        for line in docker.exec_start(cmd_id, stream=True):
            print(line.decode('ascii'), end="")

        print('Configuring permissions...')
        cmd = docker.exec_create(container_name, '/bin/sh -c "chown -R ' + str(os.getuid()) + ':' + str(os.getgid()) + ' /mnt/appimager/build"')
        docker.exec_start(cmd['Id'])
