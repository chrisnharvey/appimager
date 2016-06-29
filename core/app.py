from cement.core.foundation import CementApp
from cli import base, setup, start, stop, destroy, status, install, build, package, update

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
            update.UpdateController,
            build.BuildController,
            package.PackageController
        ]
