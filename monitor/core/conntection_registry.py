from collections import defaultdict


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class ConnectionRegistry(metaclass=SingletonMeta):
    def __init__(self):
        self.connections = {}
        self.execution_units = defaultdict(list)

    def add_connection(self, name, conn):
        self.connections[name] = conn

    def remove_connection(self, name):
        if name in self.connections:
            self.connections[name].close()
            del self.connections[name]
            print('exit {}'.format(name))

    def add_execution_unit(self, name, unit):
        self.execution_units[name].append(unit)

    def clear_execution_units(self, name):
        if name in self.execution_units:
            del self.execution_units[name]
