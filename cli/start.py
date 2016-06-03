from cli import base
from docker import Client
from core import data
from cement.core.controller import CementBaseController, expose

class StartController(CementBaseController):
    class Meta:
        label = 'start'
        stacked_on = 'base'

    @expose(help='Starts the Docker container for this environment.')
    def start(self):
        data_obj = data.Data()
        container_name = data_obj.get_path_hash()

        docker = Client()

        print('Starting container...')

        docker.start(container_name)

        print("Container started")
