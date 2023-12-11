import threading
import time


class DummySignal:
    _instance = None
    _lock = threading.Lock()

    def __init__(self):
        self.flag = False

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def acquire_lock(self):
        self._lock.acquire()
        self.flag = False

    def release_lock(self, seconds):
        time.sleep(seconds)
        self.flag = True
        self._lock.release()

    def getFlag(self):
        return self.flag