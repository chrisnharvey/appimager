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

        print('Updating APT repositories...')
        cmd = docker.exec_create(container_name, "apt-get update")
        cmd_id = cmd['Id']

        for line in docker.exec_start(cmd_id, stream=True):
            print(line.decode('ascii'), end="")

        print('Installing build dependencies...')

        build_deps = ""

        for dep in data_obj.get_build_deps():
            build_deps = build_deps + " " + dep

        cmd = docker.exec_create(container_name, "apt-get install -y " + build_deps)
        cmd_id = cmd['Id']

        for line in docker.exec_start(cmd_id, stream=True):
            print(line.decode('ascii'), end="")

        print('Setup Complete')
