import json, os
from pathlib import Path

from core import FileTypes
from core.utils import configMiss, configParamMiss

class configActions:
    def __init__(self, config_path = f"{Path.parents[3]}/config.json"):
        self.config_path = config_path
        
        self.config_base = {
            "TOKEN" : "None"
            }
        
        self.config_data = self.config_base
        
    def _checkCfg(self):
        if Path.exists(self.config_path):
            return True
        else:
            raise configMiss("Cfg miss")

    def _loadCfg(self):
        self._checkCfg()
        try:
            with open(self.config, 'r') as f:
                self.config_data = json.load(f)
            if "None" in self.config_data["TOKEN"]:
                raise configParamMiss("Invalid Token")

        except json.JSONDecodeError:
            print(f"Invalid JSON '{self.config}'")
        
        except configParamMiss as err:
            print(err)
    
    def takeCfg(self) -> dict:
        self._loadCfg()
        return self.config_data
        