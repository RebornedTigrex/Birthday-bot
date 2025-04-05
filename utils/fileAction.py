import json
import os
from typing import IO, Optional

def singleton(cls):
    instances = {}
    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return wrapper

class File:
    def __init__(self, path: str, file: Optional[IO] = None):
        self.path = path
        self.file = file
        if self.file is None:
            self.file = open(self.path, 'r')

class jsonFile(File, dict):
    def __init__(self, path: str, file: Optional[IO] = None):
        super().__init__(path, file)
        self.data = json.load(self.file)
        self.update(self.data)

@singleton
class _config(jsonFile):
    def __init__(self, path: str = "configData/config.json", file: Optional[IO] = None):
        env_config = os.getenv("CONFIG_PATH")
        if env_config:
            path = env_config
        super().__init__(path, file)