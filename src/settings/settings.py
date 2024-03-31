import configparser
from enum import Enum
from pathlib import Path
from typing import Dict

from src.settings.ini_handlers.ini_worker import IniWorker
from src.settings.ini_handlers.section import Section

""" from src.utils.file_helper.file_helper import * """
""" from src.utils.logger.logger import AppLogger """

from src.utils import *


logger = AppLogger.get_logger(__name__)


class Sections(Enum):
    localization = "Localization"
    project = "Project"

class Langs(Enum):

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))
    
    ukranian = 'ukr'
    russian = 'rus'
    english = 'eng'


class Texts(Enum):
    test_button = "Test"
    new_macros_btn = "Add macros"
    settings_btn = "Settings"
    home_btn = "Home"
    settings_page_label = "Settings Page"
    home_page_label = "Home Page"
    settings_page_lang_field = "Select the language for the app:"


class Settings:
    def __init__(self, debug_mode: bool = False):
        # __root_path - папка з проєктом
        self.__root_path: Path = Path(__file__).parent.parent.parent
        
        # __log_path - шлях до файла логів
        self.__log_path: Path = self.__root_path.joinpath('data/logs/logs.txt')

        # __localization_path - шлях до директорії з файлом локалізації
        self.__localization_path: Path = self.__root_path.joinpath('localization/')

        # __macroses_path - шлях до директорії зі збереженими скріншотами
        self.__macroses_path: Path = self.__root_path.joinpath('data/macroses/')
        
        # __config_settings_worker - воркер для роботи з файлом налаштувань
        self.__config_settings_worker: IniWorker = IniWorker(self.__root_path.joinpath('settings.ini'), configparser.ConfigParser())
        
        # __config_locale_worker - воркер для роботи з файлом локалізації
        self.__config_locale_worker: IniWorker = IniWorker(self.__root_path.joinpath(self.__localization_path, 'localization.ini'), configparser.ConfigParser())
        
        # destination_platform - платформа на якій запущений проєкт
        #self.__destination_platform: str = self._get_platform()

        self.__is_inited: bool = False

        self.__is_debug: bool = debug_mode

        self.__localization: str

        # default settings:

        self.__config_settings: Dict[str, Section] = {
            Sections.localization.value : Section(Sections.localization.value, {"lang" : Langs.english.value}),
            #Sections.project.value : Section(Sections.project.value, {"mode" : Modes.dev.value})
        }

        self.__config_locale: Dict[str, Section] = {
            Langs.english.value : Section(Langs.english.value, {Texts.test_button.name : Texts.test_button.value,
                                                                Texts.new_macros_btn.name : Texts.new_macros_btn.value,
                                                                Texts.settings_btn.name : Texts.settings_btn.value,
                                                                Texts.home_btn.name : Texts.home_btn.value,
                                                                Texts.settings_page_label.name : Texts.settings_page_label.value,
                                                                Texts.home_page_label.name : Texts.home_page_label.value,
                                                                Texts.settings_page_lang_field.name : Texts.settings_page_lang_field.value}),

        }

    @property
    def log_path(self) -> Path:
        return self.__log_path
    
    @property
    def macroses_path(self) -> Path:
        return self.__macroses_path
    
    @property
    def localization_path(self) -> Path:
        return self.__localization_path
    
    @property
    def is_inited(self) -> bool:
        return self.__is_inited
    

    def set(self, section_name: str, key: str, value: str):
        self.__config_settings_worker.set_option(section_name, key, value)
    
    def get(self, section_name: str, key: str):
        return self.__config_settings_worker.get_option(section_name, key)
    
    def save(self):
        self.__config_settings_worker.update()

    def get_ui_text(self, ui_text: Texts):
        print(self.__localization)
        return self.__config_locale_worker.get_option(self.__localization, ui_text.name)
    
    def update_locale(self, locale: str):
        self.set("Localization", "lang", locale)
        self.__localization = locale
        self.save()

    def _generate_default_settings(self):
        self.__config_settings_worker.generate_default_ini(sections=self.__config_settings.values())
        
    def _generate_default_local(self):
        self.__config_locale_worker.generate_default_ini(sections=self.__config_locale.values())

    def regenerate_defaults_files(self):
        self._generate_default_settings()
        self._generate_default_local()
    
    def init(self, debug_mode: bool = False):
        logger.info('Initialization process...')
        self.__is_debug = debug_mode
        if self.__is_debug:
            self.regenerate_defaults_files()
        else:
            if not self.__config_settings_worker.isExistINIFile():
                logger.warning(f'The settings file is missing. \
The default settings file will be created as follows: [{self.__root_path}]')
                self._generate_default_settings()
            if not self.__config_locale_worker.isExistINIFile():
                logger.warning(f'The localization file is missing. \
The default localization file will be created as follows: [{self.__localization_path}]')
                self._generate_default_local()
        
        self.__config_locale_worker.load_ini()
        self.__config_settings_worker.load_ini()
        logger.info(f"{self.__macroses_path}")
        
        if create_destination_dir(self.__macroses_path):
            logger.info('Created macroses dir')
        
        """ if create_destination_path(self.log_path):
            logger.info('Created logging file') """
       
        self.__localization = self.__config_settings_worker.get_option("Localization", "lang")
        self.__is_inited = True
    

__settingsObj = Settings()

def get_settings(debug_mode: bool = False):
    if not __settingsObj.is_inited:
        __settingsObj.init(debug_mode=debug_mode)
        
    return __settingsObj

