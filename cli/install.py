from cli import base
from core import data
import shutil
import os
import sys
import tarfile
from docker import Client
from urllib.request import urlretrieve
from cement.core.controller import CementBaseController, expose

class InstallController(CementBaseController):
    class Meta:
        label = 'install'
        stacked_on = 'base'

    @expose(help='Installs dependencies from an AppImage.yml file.')
    def install(self):
        data_obj = data.Data()
        docker = Client()

        if not os.path.exists("build"):
            print("Creating build directory")
            os.mkdir("build")

        container_name = data_obj.get_path_hash()

        print("Downloading app dependencies...")

        deps = ""

        for dep in data_obj.get_deps():
            deps = deps + " " + dep

        cmd = docker.exec_create(container_name, '/bin/sh -c "rm -rf /tmp/debs && mkdir /tmp/debs && cd /tmp/debs && apt-get download ' + deps + '"')

        for line in docker.exec_start(cmd['Id'], stream=True):
            print(line.decode('ascii'), end="")

        print('Decompressing dependencies...')

        cmd = docker.exec_create(container_name, '/bin/sh -c "ls -1 /tmp/debs | while read line ; do dpkg-deb -R /tmp/debs/$line /mnt/appimager/build ; done"')
        docker.exec_start(cmd['Id'])

        print('Configuring permissions...')
        cmd = docker.exec_create(container_name, '/bin/sh -c "chown -R ' + str(os.getuid()) + ':' + str(os.getgid()) + ' /mnt/appimager/build"')
        docker.exec_start(cmd['Id'])

        shutil.rmtree('build/DEBIAN')

        print("Complete")
