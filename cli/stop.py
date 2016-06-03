from cli import base
from cement.core.controller import CementBaseController, expose

class StopController(CementBaseController):
    class Meta:
        label = 'stop'
        stacked_on = 'base'

    @expose(help='Stops the Docker container for this environment.')
    def stop(self):
        self.app.log.info("Stop command")
