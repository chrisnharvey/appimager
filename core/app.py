from cement.core.foundation import CementApp
from cli import base, setup, install, package

class AppImager(CementApp):
    class Meta:
        label = 'appimager'
        base_controller = 'base'
        handlers = [base.BaseController, setup.SetupController, install.InstallController, package.PackageController]
