from controllers import base
from cement.core.controller import CementBaseController, expose

class InstallController(CementBaseController):
    class Meta:
        label = 'install'
        stacked_on = 'base'

    @expose(help='Installs dependencies from an AppImage.yml file.')
    def install(self):
        self.app.log.info("Install command")
