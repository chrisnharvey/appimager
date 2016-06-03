from cement.core.foundation import CementApp
from cli import base, setup, start, stop, destroy, status, install, package

class AppImager(CementApp):
    class Meta:
        label = 'appimager'
        base_controller = 'base'
        handlers = [
            base.BaseController,
            setup.SetupController,
            start.StartController,
            stop.StopController,
            destroy.DestroyController,
            status.StatusController,
            install.InstallController,
            package.PackageController
        ]
