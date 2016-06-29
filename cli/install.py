from cli import base
from core import data, container
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
        build_path = data_obj.get_build_path()
        docker = Client()

        if not os.path.exists(build_path):
            print("Creating build directory")
            os.mkdir(build_path)

        container_name = data_obj.get_path_hash()
        container_obj = container.Container(container_name)

        print("Downloading app dependencies...")

        deps = ""

        for dep in data_obj.get_deps():
            deps = deps + " " + dep

        for line in container_obj.execute('rm -rf /tmp/debs && mkdir /tmp/debs && cd /tmp/debs && apt-get download ' + deps):
            print(line, end="")

        print('Decompressing dependencies...')

        container_obj.execute('ls -1 /tmp/debs | while read line ; do dpkg-deb -R /tmp/debs/$line /mnt/appimager/build ; done')

        print('Configuring permissions...')
        container_obj.execute('chown -R ' + str(os.getuid()) + ':' + str(os.getgid()) + ' /mnt/appimager/build')

        shutil.rmtree('build/DEBIAN')

        print('Writing lock file...')
        data_obj.write_lock_file()

        print("Complete")
