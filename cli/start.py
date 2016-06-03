from cli import base
from cement.core.controller import CementBaseController, expose

class StartController(CementBaseController):
    class Meta:
        label = 'start'
        stacked_on = 'base'

    @expose(help='Starts the docker container for this environment')
    def start(self):
        self.app.log.info("Start command")
