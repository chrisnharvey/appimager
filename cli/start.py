from cli import base
from docker import Client
from core import data, container
from cement.core.controller import CementBaseController, expose

class StartController(CementBaseController):
    class Meta:
        label = 'start'
        stacked_on = 'base'

    @expose(help='Starts the Docker container for this environment.')
    def start(self):
        data_obj = data.Data()
        container_name = data_obj.get_path_hash()

        docker = container.Container(container_name)

        print('Starting container...')

        docker.start()

        print("Container started")
