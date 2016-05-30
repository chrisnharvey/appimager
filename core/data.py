import os
import yaml

class Data:
    def get_build_path(self):
        cwd = os.getcwd()
        default = cwd + "/build"

        yaml_data = self.get_yml_data()

        if 'build_path' in yaml_data:
            return cwd + '/' + yaml_data['build_path']

        return default

    def get_yml_data(self):
        file_path = os.getcwd() + "/AppImage.yml"

        stream = open(file_path, 'r')

        return yaml.load(stream)
