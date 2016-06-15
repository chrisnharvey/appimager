from cement.core.controller import CementBaseController, expose

class BaseController(CementBaseController):
    class Meta:
        label = 'base'
        description = "AppImager provides a build environment and tools for managing AppImage dependencies, assisting in the creation of AppDir's and creating AppImages from source code."


    @expose(hide=True)
    def default(self):
        self.app.args.print_help()
