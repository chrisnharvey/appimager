from cli import base
from docker import Client
from core import data, container
from cement.core.controller import CementBaseController, expose

class StopController(CementBaseController):
    class Meta:
        label = 'stop'
        stacked_on = 'base'

    @expose(help='Stops the Docker container for this environment.')
    def stop(self):
        data_obj = data.Data()
        container_name = data_obj.get_path_hash()
        container_obj = container.Container(container_name)

        print('Stopping container...')

        container_obj.stop()

        print("Container stopped")
