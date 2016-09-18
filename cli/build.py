import os
from docker import Client
from core import data, container
from cement.core.controller import CementBaseController, expose

class BuildController(CementBaseController):
    class Meta:
        label = 'build'
        stacked_on = 'base'

    @expose(help='Run the build command/script to compile your application.')
    def build(self):
        data_obj = data.Data()
        container_name = data_obj.get_path_hash()
        container_obj = container.Container(container_name)
        yml_data = data_obj.get_yml_data()

        for line in container_obj.execute('cd /mnt/appimager/cwd && ' + yml_data['build']):
            print(line, end="")

        if 'integration' in yml_data.keys():
            print('Setting up desktop integration...')
            for line in container_obj.execute('wget -O /mnt/appimager/build/' + yml_data['integration'] + '.wrapper https://raw.githubusercontent.com/probonopd/AppImageKit/master/desktopintegration'):
                print(line)

            for line in container_obj.execute('chmod +x /mnt/appimager/build/' + yml_data['integration'] + '.wrapper'):
                print(line)

        print('Configuring permissions...')
        container_obj.execute('chown -R ' + str(os.getuid()) + ':' + str(os.getgid()) + ' /mnt/appimager/build')
