from cli import base
from cement.core.controller import CementBaseController, expose

class BuildController(CementBaseController):
    class Meta:
        label = 'build'
        stacked_on = 'base'

    @expose(help='Run the build command/script to compile your application.')
    def build(self):
        self.app.log.info("Build command")
