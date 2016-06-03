from cli import base
from cement.core.controller import CementBaseController, expose

class DestroyController(CementBaseController):
    class Meta:
        label = 'destroy'
        stacked_on = 'base'

    @expose(help='Destroys the docker container for this environment')
    def destroy(self):
        self.app.log.info("Destroy command")
