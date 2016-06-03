from cli import base
from cement.core.controller import CementBaseController, expose

class StatusController(CementBaseController):
    class Meta:
        label = 'status'
        stacked_on = 'base'

    @expose(help='Shows the status of the docker container for this environment')
    def status(self):
        self.app.log.info("Status command")
