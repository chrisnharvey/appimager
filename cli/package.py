from __future__ import division
from cli import base
from core import data
from cement.core.controller import CementBaseController, expose
import os, sys
import subprocess
from core import xdgappdir
from locale import gettext as _

class PackageController(CementBaseController):
    class Meta:
        label = 'package'
        stacked_on = 'base'

    @expose(help='Package AppDir into an AppImage.')
    def package(self):
        data_obj = data.Data()
        path = data_obj.get_work_path()

        # Also search for dependency binaries and libraries next to myself
        dependenciesdir = path + "/usr/"
        os.environ['PATH'] =  dependenciesdir + "/bin:" + os.getenv('PATH')
        # print os.environ['PATH']
        lddp = os.getenv('LD_LIBRARY_PATH')
        if lddp == None: lddp = ""
        os.environ['LD_LIBRARY_PATH'] =  dependenciesdir + "/lib:" + lddp

        sourcedir = path
        destinationfile = data_obj.get_out_path()
        should_compress = True

        if should_compress == True:
            if not os.path.exists(sourcedir):
                print("Application work directory not found: %s" % (sourcedir))
                exit(1)

        if should_compress == True:
            H = xdgappdir.AppDirXdgHandler(sourcedir)
            iconfile = H.get_icon_path_by_icon_name(H.get_icon_name_from_desktop_file(H.desktopfile))
            if iconfile == None:
                print("Icon could not be found based on information in desktop file")
                #exit(1)

            print("Creating %s..." % (destinationfile))
            if os.path.exists(destinationfile):
                print (_("Destination path already exists, exiting")) # xorriso would append another session to a pre-existing image
                exit(1)
            # As great as xorriso is, as cryptic its usage is :-(
            command = ["xorriso", "-joliet", "on", "-volid", "AppImage", "-dev",
            destinationfile, "-padding", "0", "-map",
            sourcedir, "/", "--", "-map", iconfile, "/.DirIcon",
            "-zisofs", "level=9:block_size=128k:by_magic=off", "-chown_r", "0",
            "/", "--", "set_filter_r", "--zisofs", "/" ]

            subprocess.Popen(command).communicate()

            print("ok")

        print("Embedding runtime...")
        elf = os.path.realpath(os.path.dirname(__file__)) + "/runtime"
        s = open(elf, 'rb')
        f = open(destinationfile, 'rb+')
        f.write(bytes(s.read()))
        f.close()
        s.close()
        print("ok")

        print("Making %s executable..." % (destinationfile))

        os.chmod(destinationfile, 0o755)

        print("ok")

        filesize = int(os.stat(destinationfile).st_size)
        print (_("Size: %f MB") % (filesize/1024/1024))
