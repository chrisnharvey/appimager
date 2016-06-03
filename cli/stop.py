from cli import base
from docker import Client
from core import data
from cement.core.controller import CementBaseController, expose

class StopController(CementBaseController):
    class Meta:
        label = 'stop'
        stacked_on = 'base'

    @expose(help='Stops the Docker container for this environment.')
    def stop(self):
        data_obj = data.Data()
        container_name = data_obj.get_path_hash()

        docker = Client()

        print('Stopping container...')

        docker.stop(container_name)

        print("Container stopped")
