from cli import base
from core import data, container
import shutil
import os
import sys
import tarfile
from docker import Client
from urllib.request import urlretrieve
from cement.core.controller import CementBaseController, expose

class UpdateController(CementBaseController):
    class Meta:
        label = 'update'
        stacked_on = 'base'

    @expose(help='Update dependencies from an AppImage.yml file.')
    def update(self):
        data_obj = data.Data()
        build_path = data_obj.get_build_path()
        docker = Client()

        container_name = data_obj.get_path_hash()
        container_obj = container.Container(container_name)

        print('Installing new build dependencies...')

        build_deps = ""

        for dep in data_obj.get_build_deps_to_install():
            build_deps = build_deps + " " + dep

        for line in container_obj.execute("apt-get install -y " + build_deps):
            print(line, end="")

        print('Removing old build dependencies...')

        build_deps = ""

        for dep in data_obj.get_build_deps_to_remove():
            build_deps = build_deps + " " + dep

        for line in container_obj.execute("apt-get purge -y " + build_deps):
            print(line, end="")

        print('Removing orphaned dependencies...')

        for line in container_obj.execute("apt-get autoremove -y"):
            print(line, end="")

        print("Installing new app dependencies...")

        deps = ""

        for dep in data_obj.get_deps_to_install():
            deps = deps + " " + dep

        for line in container_obj.execute('rm -rf /tmp/debs && mkdir /tmp/debs && cd /tmp/debs && apt-get download ' + deps):
            print(line, end="")

        print('Decompressing new dependencies...')

        container_obj.execute('ls -1 /tmp/debs | while read line ; do dpkg-deb -R /tmp/debs/$line /mnt/appimager/build ; done')

        print('Removing old dependencies...')

        container_obj.execute('ls -1 /tmp/debs | while read line ; do dpkg-deb -R /tmp/debs/$line /mnt/appimager/build ; done')

        print('Configuring permissions...')
        container_obj.execute('chown -R ' + str(os.getuid()) + ':' + str(os.getgid()) + ' /mnt/appimager/build')

        shutil.rmtree('build/DEBIAN')

        print('Writing lock file...')
        data_obj.write_lock_file()

        print("Complete")
