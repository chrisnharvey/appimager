from controllers import base
from cement.core.controller import CementBaseController, expose

class PackageController(CementBaseController):
    class Meta:
        label = 'package'
        stacked_on = 'base'

    @expose(help='Package AppDir into an AppImage.')
    def package(self):
        self.app.log.info("Package command")
