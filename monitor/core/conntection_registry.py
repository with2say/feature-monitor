from threading import Lock

class SingletonMeta(type):
    _instances = {}
    _lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]

class ConnectionRegistry(metaclass=SingletonMeta):
    def __init__(self):
        self.connections = {}
        self._lock = Lock()

    def add_connection(self, name, conn):
        with self._lock:
            if name in self.connections:
                self.connections[name].append(conn)
            else:
                self.connections[name] = [conn]
        print(len(self.connections), self.connections)

    def stop_connection(self, name):
        with self._lock:
            if name in self.connections:
                for conn in self.connections[name]:
                    conn.close()
                del self.connections[name]
        print('Stopping... {}'.format(name))
