import os
import hashlib
import yaml
import platform

class Data:
    def get_build_path(self):
        return self.get_path('build')

    def get_out_path(self):
        return self.get_path('out')

    def get_path_hash(self, key=''):
        return hashlib.md5(self.get_path(key).encode('utf-8')).hexdigest()

    def get_path(self, key=''):
        cwd = os.getcwd()
        default = cwd + "/" + key

        yaml_key = key + '_path'
        yaml_data = self.get_yml_data()

        if yaml_key in yaml_data:
            return cwd + '/' + yaml_data[yaml_key]

        return default

    def get_yml_data(self):
        file_path = os.getcwd() + "/AppImage.yml"

        stream = open(file_path, 'r')

        return yaml.load(stream)

    def get_deps(self):
        yml = self.get_yml_data()

        if not hasattr(yml, 'require'):
            return []

        deps = yml['require']

        if deps == None:
            return []

        return deps

    def get_build_deps(self):
        yml = self.get_yml_data()

        if not hasattr(yml, 'require_build'):
            return []

        deps = yml['require_build']

        if deps == None:
            return []

        return deps

    def get_env_vars(self):
        yml = self.get_yml_data()

        default_env = {
            'LD_LIBRARY_PATH': '/mnt/appimager/build/lib:/mnt/appimager/build/lib32:/mnt/appimager/build/lib64:/mnt/appimager/build/lib/i386-linux-gnu:/mnt/appimager/build/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH',
            'PATH': '/mnt/appimager/build/bin:$PATH',
            'PKG_CONFIG_PATH': '/mnt/appimager/build/lib/pkgconfig:$PKG_CONFIG_PATH',
            'PYTHONPATH': '/mnt/appimager/build/share/pyshared:$PYTHONPATH',
            'XDG_DATA_DIRS': '/mnt/appimager/build/:$XDG_DATA_DIRS',
            'QT_PLUGIN_PATH': '/mnt/appimager/build/lib/qt4/plugins:/mnt/appimager/build/lib/qt5/plugins:$QT_PLUGIN_PATH',
            'PERLLIB': '/mnt/appimager/build/share/perl5:/mnt/appimager/build/lib/perl5:$PERLLIB'
        }

        if not hasattr(yml, 'env'):
            return default_env

        env = yml['env']

        if env == None:
            return default_env

        for var, value in env:
            if not hasattr(default_env, var):
                env_vars[var] = value
            else:
                env_vars[var] = default_env[var] + ':' + value

        return env_vars

    def get_env_vars_string(self):
        env_string = ''

        for env, value in self.get_env_vars().items():
            env_string = env_string + "; " + env + '="' + value + '"'

        return env_string.strip('; ')

    def architecture(self):
        arch = platform.architecture()[0]

        if arch == '64bit':
            return 'x86_64'

        return 'i386'
