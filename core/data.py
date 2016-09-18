import os
import hashlib
import yaml
import platform

class Data:
    def get_build_path(self):
        return self.get_path('build')

    def get_out_path(self):
        return self.get_path('out')

    def get_work_path(self):
        return self.get_path('work')

    def get_path_hash(self, key=''):
        return hashlib.md5(self.get_path(key).encode('utf-8')).hexdigest()

    def write_lock_file(self, data=False):
        if not data:
            data = self.get_yml_data()

        current_data = self.get_lock_data()
        new_data = current_data

        for key, value in data.items():
            new_data[key] = value

        file_path = os.getcwd() + "/AppImage.lock"
        lock_file = open(file_path, 'w')

        yaml.dump(new_data, lock_file)

    def get_path(self, key=''):
        cwd = os.getcwd()
        default = cwd + "/" + key

        yaml_key = key + '_path'
        yaml_data = self.get_yml_data()

        if yaml_key in yaml_data:
            return cwd + '/' + yaml_data[yaml_key]

        return default

    def get_lock_data(self):
        file_path = os.getcwd() + "/AppImage.lock"

        if not os.path.isfile(file_path):
            return {}

        stream = open(file_path, 'r')

        return yaml.load(stream)

    def get_yml_data(self):
        file_path = os.getcwd() + "/AppImage.yml"

        stream = open(file_path, 'r')

        return yaml.load(stream)

    def get_deps(self):
        return self.get_yml_key('require')

    def get_lock_deps(self):
        return self.get_lock_key('require')

    def get_yml_key(self, key):
        yml = self.get_yml_data()

        if not key in yml:
            return []

        value = yml[key]

        if value == None:
            return []

        return value

    def get_lock_key(self, key):
        yml = self.get_lock_data()

        if not key in yml:
            return []

        value = yml[key]

        if value == None:
            return []

        return value

    def get_deps_to_install(self):
        return list(set(self.get_deps()) - set(self.get_lock_deps()))

    def get_deps_to_remove(self):
        matched = list(set(self.get_lock_deps()).intersection(set(self.get_deps())))
        return list(set(self.get_lock_deps()) - set(matched))

    def get_build_deps_to_remove(self):
        matched = list(set(self.get_build_lock_deps()).intersection(set(self.get_build_deps())))
        return list(set(self.get_build_lock_deps()) - set(matched))

    def get_build_deps_to_install(self):
        return list(set(self.get_build_deps()) - set(self.get_build_lock_deps()))

    def get_repositories(self):
        return self.get_yml_key('repositories')

    def get_build_deps(self):
        return self.get_yml_key('require_build')

    def get_build_lock_deps(self):
        return self.get_lock_key('require_build')

    def get_env_vars(self):
        yml = self.get_yml_data()

        default_env = {
            'LD_LIBRARY_PATH': '/mnt/appimager/build/lib/:/mnt/appimager/build/lib32/:/mnt/appimager/build/lib64/:/mnt/appimager/build/lib/i386-linux-gnu/:/mnt/appimager/build/lib/x86_64-linux-gnu/:$LD_LIBRARY_PATH',
            'PATH': '/mnt/appimager/build/bin/:$PATH',
            'PKG_CONFIG_PATH': '/mnt/appimager/build/lib/pkgconfig/:$PKG_CONFIG_PATH',
            'PYTHONPATH': '/mnt/appimager/build/share/pyshared/:$PYTHONPATH',
            'XDG_DATA_DIRS': '/mnt/appimager/build/:$XDG_DATA_DIRS',
            'QT_PLUGIN_PATH': '/mnt/appimager/build/lib/qt4/plugins/:/mnt/appimager/build/lib/qt5/plugins/:$QT_PLUGIN_PATH',
            'PERLLIB': '/mnt/appimager/build/share/perl5/:/mnt/appimager/build/lib/perl5/:$PERLLIB',
            'GSETTINGS_SCHEMA_DIR': '/mnt/appimager/build/share/glib-2.0/schemas/:$GSETTINGS_SCHEMA_DIR',
            # 'PKG_CONFIG_LIBDIR': '/mnt/appimager/build/lib/pkgconfig/:$PKG_CONFIG_LIBDIR',
            'CFLAGS': '-I/mnt/appimager/build/include',
            'LDFLAGS': '-L/mnt/appimager/build/lib'
        }

        if not 'env' in yml:
            return default_env

        env = yml['env']

        if env == None:
            return default_env

        for var, value in env:
            if not var in default_env:
                env_vars[var] = value
            else:
                env_vars[var] = default_env[var] + ':' + value

        return env_vars

    def get_env_vars_string(self, export: bool):
        env_string = ''

        for env, value in self.get_env_vars().items():
            if (export):
                env = 'export ' + env

            env_string = env_string + "; " + env + '="' + value + '"'

        return env_string.strip('; ')

    def architecture(self):
        arch = platform.architecture()[0]

        if arch == '64bit':
            return 'x86_64'

        return 'i686'
