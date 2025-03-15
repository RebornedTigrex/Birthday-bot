import json
from pathlib import Path

# Всё это ебучий код ради кода. Потом нужно будет переделать, либо перевести всё на библиотеку config 

class configActions:
    def __init__(self, config_path = "configData/config.json"):
        self.config_path = config_path
        
        # Если проебать конфиг - весь бот нахуй упадёт и не встанет.
        # TODO: Добавить автоматическое создание и поиск конфига при его отсутствии
        self.config_base = {
            "TOKEN" : "None",
            "dbLocation" : "userData/birthdays.json"
            }
        
        self.config_data = self.config_base
        
    def _checkCfg(self):
        if Path.exists(self.config_path):
            return True
        else:
            raise Exception("Cfg miss")

    def _loadCfg(self):
        self._checkCfg()
        try:
            with open(self.config, 'r') as f:
                self.config_data = json.load(f)
            if "None" in self.config_data["TOKEN"]:
                raise Exception("Invalid Token or Token in config = None")

        except json.JSONDecodeError:
            print(f"Invalid JSON '{self.config}'")
            
        except Exception as err:
            print(err)
    
    def takeCfg(self) -> dict:
        self._loadCfg()
        return self.config_data
    
    def takeParam(self, param:str) -> str|list[str]:
        self._loadCfg()
        return self.config_data[param]
        