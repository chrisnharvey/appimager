from cement.core.controller import CementBaseController, expose

class BaseController(CementBaseController):
    class Meta:
        label = 'base'
        description = "AppImager can manage AppImage dependencies, assist in the creation of AppDir's and create AppImages from source code"
