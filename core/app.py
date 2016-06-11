from cement.core.foundation import CementApp
from cli import base, setup, start, stop, destroy, status, install, build, package

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
            build.BuildController,
            package.PackageController
        ]
