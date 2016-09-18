from cli import base
from core import data, container
from cement.core.controller import CementBaseController, expose

class PackageController(CementBaseController):
    class Meta:
        label = 'package'
        stacked_on = 'base'

    @expose(help='Package the AppDir into an AppImage.')
    def package(self):
        data_obj = data.Data()
        container_name = data_obj.get_path_hash()
        container_obj = container.Container(container_name)

        for line in container_obj.execute('AppImageAssistant.AppImage /mnt/appimager/build /mnt/appimager/out/' + data_obj.get_name()):
            print(line, end="")
