from controllers import base
from cement.core.controller import CementBaseController, expose

class SetupController(CementBaseController):
    class Meta:
        label = 'setup'
        stacked_on = 'base'

    @expose(help='Sets up a docker container for building AppImages.')
    def setup(self):
        self.app.log.info("Setup command")
