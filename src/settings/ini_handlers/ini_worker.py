from configparser import ConfigParser
from pathlib import Path
from typing import Dict

from src.settings.ini_handlers.section import Section

from src.utils.logger.logger import AppLogger
from src.utils.file_helper.file_helper import create_destination_path

logger = AppLogger.get_logger(__name__)


class IniWorker:
    def __init__(self, path_to_file: str, parser: ConfigParser):
        
        self.__parser: ConfigParser = parser
        self.__path_to_file: str = path_to_file

        self.__cache: Dict[str, object] = {}

    def _isINIFile(self, path_to_file: str) -> bool:
        checkable_path = Path(path_to_file)
        if Path.is_file(checkable_path) and checkable_path.suffix == ".ini":
            return True
        return False
    
    def isExistINIFile(self) -> bool:
        return self._isINIFile(self.__path_to_file)
    
    
    def generate_default_ini(self, sections: list[Section]) -> bool:
        '''
        generate_default_ini - це допоміжна функція для генерації шаблону settings.ini 
        з дефолтними значеннями
        '''
        logger.info('Generate Default ini...')
        if not self._isINIFile(self.__path_to_file):
            #Path.touch(self.__path_to_file)
            create_destination_path(self.__path_to_file)
        
        default_ini = ConfigParser()
        
        try:
            for section in sections:
                default_ini.add_section(section.name)
                try: 
                    atr = section.settings
                    for key, value in atr.items():
                        default_ini.set(section.name, key, value)
                except:
                    logger.error(f"Error. Can't to set section with class attribute values. \
Used method ConfigParser.set() with [{section.name}] section, key type: {type(key)} and value type: {type(value)}")
                
                    return False
        except:
            logger.error(f"Error. Can't to prepare ConfigParser")
            return False

        with open(f'{self.__path_to_file}', 'w') as f:
            logger.warning(f'A new file was created at the path: {self.__path_to_file}')
            default_ini.write(f)    
        return True
          
    def load_ini(self):
        logger.debug("Loading ini file...")
        self.__parser.read(self.__path_to_file, encoding='utf-8')
        
    def add_section(self, section: Section):
        self.__parser.add_section(section.name)
        for key, value in section.settings.items():
            self.__parser.set(section.name, key, value)

    def get_section(self, section_name: str) -> Section:
        data = self.get_settings_from_section(section_name)
        return Section(section_name, data)
    
    def get_all_sections(self) -> list[Section]:
        data = self.get_all_settings()
        sections = []
        for key, value in data.items():
            sections.append(Section(key, value))
        
        return sections
    
    def get_settings_from_section(self, section_name: str) -> Dict[str, str]:
        values = {}
        for key, value in self.__parser.items(section=section_name):
            values[key] = value
            
        return values
    
    def get_all_settings(self) -> Dict[str, Dict[str, str]]:  
        data = {}
        for section in self.__parser.sections:
                values = {}
                for key, value in self.__parser.items(section):
                    values[key] = value
                data[section] = values
        return data
        
    def remove_section(self, section_name: str):
        self.__parser.remove_section(section_name)
    
    def clear(self):
        self.__parser.clear()
        
    def set_option(self, section_name: str, key: str, value: str):
        self.__parser.set(section_name, key, value)

    def remove_option(self, section_name: str, key: str):
        self.__parser.remove_option(section_name, key)

    def get_option(self, section_name: str, key: str) -> str:
        return self.__parser.get(section_name, key)

    def update(self):
        for key, value in self.__parser.items():
            print(f"{key} : {value}")
        with open(f'{self.__path_to_file}', 'w') as f:
            self.__parser.write(f)

    def update_from_sections(self, sections: list[Section]):
        parser = self.__parser
        for section in sections:
            parser.update()
        with open(f'{self.__path_to_file}', 'w') as f:
            self.__parser.write(f)

