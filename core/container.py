import os
from docker import Client
from core import data

class Container:
    def __init__(self, name):
        self.name = name

        self.docker = Client()

    def start(self):
        return self.docker.start(self.name)

    def stop(self):
        return self.docker.stop(self.name)

    def execute(self, command):
        data_obj = data.Data()

        cmd = self.docker.exec_create(self.name, '/bin/sh -c "' + data_obj.get_env_vars_string(True) + ' && ' + command + '"')
        cmd_id = cmd['Id']

        for line in self.docker.exec_start(cmd_id, stream=True):
            yield(line.decode('ascii'))

    def restart(self):
        return self.docker.restart(self.name)

    def status(self):
        return self.docker.status(self.name)

    def destroy(self):
        return self.docker.remove_container(self.name)
