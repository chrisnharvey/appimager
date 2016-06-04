from cli import base
from core import data
import sys
from urllib.request import urlretrieve
from cement.core.controller import CementBaseController, expose

class InstallController(CementBaseController):
    class Meta:
        label = 'install'
        stacked_on = 'base'

    @expose(help='Installs dependencies from an AppImage.yml file.')
    def install(self):
        data_obj = data.Data()
        yaml = data_obj.get_yml_data()

        arch = data_obj.architecture()

        print("Downloading app dependencies...")

        for package, version in yaml['require'].items():
            url = "https://archive.archlinux.org/packages/" + package[0] + "/" + package + "/" + package + "-" + version + "-" + arch + ".pkg.tar.xz"

            def reporthook(blocknum, blocksize, totalsize):
                readsofar = blocknum * blocksize
                if totalsize > 0:
                    percent = readsofar * 1e2 / totalsize
                    s = "\rDownloading " + package + " (" + version + ") %5.1f%% %*d / %dK" % (
                        percent, len(str(totalsize)), readsofar / 1024, totalsize / 1024)
                    sys.stderr.write(s)
                    if readsofar >= totalsize: # near the end
                        sys.stderr.write("\n")
                else: # total size is unknown
                    sys.stderr.write("read %d\n" % (readsofar,))

            urlretrieve(url, package + ".tar.xz", reporthook)

        print("Complete")
