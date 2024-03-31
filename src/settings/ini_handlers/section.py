from configparser import ConfigParser
from typing import Dict


class Section:
    def __init__(self, name: str, settings: Dict[str, str] = {}):
        self.__name: str = name
        self.__settings: Dict[str, str] = settings
        

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Section):
            return False
        return self.name == other.name

    @property
    def name(self):
        return self.__name
    
    @property
    def settings(self):
        return self.__settings