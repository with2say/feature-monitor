

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

    def add_connection(self, name, conn):
        if name in self.connections:
            self.connections[name].append(conn)
        else:
            self.connections[name] = [conn]
        print(len(self.connections), self.connections)

    def stop_connection(self, name):
        print(self.connections)
        if name in self.connections:
            for conn in self.connections[name]:
                conn.close()
            del self.connections[name]
            print('Stopping... {}'.format(name))

