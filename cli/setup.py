from cli import base
from core import data, container
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
        yml = data_obj.get_yml_data()

        docker = Client()

        print('Setting up environment, please wait...')

        volume = os.getcwd()

        base_os_version = yml['base']
        container_name = data_obj.get_path_hash()

        container_obj = container.Container(container_name)

        print('Pulling Ubuntu ' + str(base_os_version) + '...')
        docker.pull('ubuntu', str(base_os_version))

        data_obj = data.Data()

        print('Creating container...')
        docker.create_container('ubuntu:' + str(base_os_version), tty=True, command="/bin/bash", name=container_name, volumes=['/mnt/appimager'],
            host_config=docker.create_host_config(privileged=True, cap_add=['SYS_ADMIN'], binds={
                os.getcwd(): {
                    'bind': '/mnt/appimager/work',
                    'mode': 'ro',
                },
                data_obj.get_build_path(): {
                    'bind': '/mnt/appimager/build',
                    'mode': 'rw',
                },
                data_obj.get_out_path(): {
                    'bind': '/mnt/appimager/out',
                    'mode': 'rw',
                }
            }))

        print('Starting container...')
        container_obj.start()

        print('Updating APT repositories...')

        for line in container_obj.execute("apt-get update"):
            print(line, end="")

        print('Installing common dependencies...')
        for line in container_obj.execute('apt-get -y install software-properties-common python-software-properties wget'):
            print(line, end="")

        print('Downloading AppImageAssistant...')
        for line in container_obj.execute('wget -O /usr/bin/AppImageAssistant.AppImage https://github.com/probonopd/AppImageKit/releases/download/6/AppImageAssistant_6-' + data_obj.architecture() + '.AppImage && chmod +x /usr/bin/AppImageAssistant.AppImage'):
            print(line, end="")

        print('Adding additional APT repositories...')
        for repo in data_obj.get_repositories():
            for line in container_obj.execute('add-apt-repository -y ' + repo):
                print(line, end="")

        print('Updating APT repositories...')

        for line in container_obj.execute("apt-get update"):
            print(line, end="")

        print('Installing build dependencies...')

        build_deps = ""

        for dep in data_obj.get_build_deps():
            build_deps = build_deps + " " + dep

        for line in container_obj.execute("apt-get install -y " + build_deps):
            print(line, end="")

        print('Writing lock file...')
        data_obj.write_lock_file()

        print('Setup Complete')
