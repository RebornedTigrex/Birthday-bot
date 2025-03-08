import json, os
from pathlib import Path

from core import FileTypes

class configActions:
    def __init__(self, config_path = f"{Path.parents[4]}/config.json"):
        self.config_path = config_path
        
        self.config_base = {
            "TOKEN" : "N"
            }
        
        
        
        self.config_data = self.config_base
        
    def _checkCfg(self):
        if Path.exists(self.config_path):
            return True
        else:
            raise 
        
        
    
    def loadCfg(self):
        try:
            with open(self.config, 'r') as f:
                self.config_data = json.load(f)
            
            # if "parce_type" not in self.config_data:
            #     raise Exception("ParamDoestExist:1:", "Configuration parameter 'parce_type' is missing. 'parce_type' set to default value.")
            # if "arg" not in self.config_data:
            #     raise Exception("ParamDoestExist:2:", "Configuration parameter 'arg' is missing. 'arg' set to default value.")
            
        except json.JSONDecodeError:
            print(f"Invalid JSON'{self.config}' or file does not exist. Script is using default configuration.")
            
        except Exception as err:
            print(f"Panic! In metood {self._load_config.__name__}: {err.args}")
            # if err.args[0] == "ParamDoestExist:1:":
            #     self.config_data["parce_type"] = self.config_base["parce_type"]
            # if err.args[0] == "ParamDoestExist:2:":
            #     self.config_data["arg"] = self.config_base["arg"]