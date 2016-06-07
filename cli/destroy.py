from cli import base
from core import data
from docker import Client
from cement.core.controller import CementBaseController, expose

class DestroyController(CementBaseController):
    class Meta:
        label = 'destroy'
        stacked_on = 'base'

    @expose(help='Destroys the Docker container for this environment.')
    def destroy(self):
        data_obj = data.Data()
        container_name = data_obj.get_path_hash()

        docker = Client()

        print('Stopping container...')

        docker.stop(container_name)

        print('Destroying container...')

        docker.remove_container(container_name)

        print("Container destroyed")
