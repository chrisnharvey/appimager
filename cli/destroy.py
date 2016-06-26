from cli import base
from core import data, container
from cement.core.controller import CementBaseController, expose

class DestroyController(CementBaseController):
    class Meta:
        label = 'destroy'
        stacked_on = 'base'

    @expose(help='Destroys the Docker container for this environment.')
    def destroy(self):
        data_obj = data.Data()
        container_name = data_obj.get_path_hash()
        container_obj = container.Container(container_name)

        print('Stopping container...')

        container_obj.stop()

        print('Destroying container...')

        container_obj.destroy()

        print("Container destroyed")
