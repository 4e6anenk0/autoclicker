import configparser
from enum import Enum
from pathlib import Path
from typing import Dict

from src.settings.ini_handlers.ini_worker import IniWorker
from src.settings.ini_handlers.section import Section

from src.utils.logger.logger import AppLogger

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
    macroses_viewer_btn = "My macroses"
    
    settings_page_label = "Settings Page"
    home_page_label = "Home Page"
    settings_page_lang_field = "Select the language for the app:"
    macros_editor_save_macros_button = "Save macros"
    macros_editor_title_placeholder = "Macros name"
    macros_editor_no_info_label = "No any nodes..."
    macros_editor_type_node_menu_placeholder = "Node type:"
    macros_editor_add_node_button = "Add node"
    macros_editor_name_entry_placeholder = "Node name..."
    macros_editor_desc_entry_label = "Description:"
    
    macros_editor_clean_btn = "Clean"

    macros_viewer_choose_btn = "Choose"
    macros_viewer_decline_btn = "Decline"
    macros_viewer_remove_btn = "Remove"
    macros_viewer_label_text = "Name: "
    macros_viewer_run_btn = "Run"
    macros_viewer_load_more_btn = "Load more..."
    macros_viewer_loaded_label = "End..."

    node_views_type_of_button = "Mouse key type:"
    node_views_number_of_click = "Clicks:"
    node_views_show_move = "Show movement:"

    remove_alert_confirm = "Yes"
    remove_alert_discard = "No"
    remove_alert_msg = "Do you want to delete this node?"

    media_view_no_media = "No media"

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
                                                                Texts.macroses_viewer_btn.name : Texts.macroses_viewer_btn.value,
                                                                Texts.settings_page_label.name : Texts.settings_page_label.value,
                                                                Texts.home_page_label.name : Texts.home_page_label.value,
                                                                Texts.settings_page_lang_field.name : Texts.settings_page_lang_field.value,
                                                                Texts.macros_editor_add_node_button.name : Texts.macros_editor_add_node_button.value,
                                                                Texts.macros_editor_desc_entry_label.name : Texts.macros_editor_desc_entry_label.value,
                                                                Texts.macros_editor_name_entry_placeholder.name : Texts.macros_editor_name_entry_placeholder.value,
                                                                Texts.macros_editor_no_info_label.name : Texts.macros_editor_no_info_label.value,
                                                                Texts.macros_editor_save_macros_button.name : Texts.macros_editor_save_macros_button.value,
                                                                Texts.macros_editor_title_placeholder.name : Texts.macros_editor_title_placeholder.value,
                                                                Texts.macros_editor_type_node_menu_placeholder.name : Texts.macros_editor_type_node_menu_placeholder.value,
                                                                Texts.macros_editor_clean_btn.name : Texts.macros_editor_clean_btn.value,
                                                                Texts.macros_viewer_choose_btn.name : Texts.macros_viewer_choose_btn.value,
                                                                Texts.macros_viewer_decline_btn.name : Texts.macros_viewer_decline_btn.value,
                                                                Texts.macros_viewer_remove_btn.name : Texts.macros_viewer_remove_btn.value,
                                                                Texts.macros_viewer_label_text.name : Texts.macros_viewer_label_text.value,
                                                                Texts.macros_viewer_run_btn.name : Texts.macros_viewer_run_btn.value,
                                                                Texts.macros_viewer_load_more_btn.name : Texts.macros_viewer_load_more_btn.value,
                                                                Texts.macros_viewer_loaded_label.name : Texts.macros_viewer_loaded_label.value,
                                                                Texts.node_views_number_of_click.name : Texts.node_views_number_of_click.value,
                                                                Texts.node_views_show_move.name : Texts.node_views_show_move.value,
                                                                Texts.node_views_type_of_button.name : Texts.node_views_type_of_button.value,
                                                                Texts.remove_alert_confirm.name : Texts.remove_alert_confirm.value,
                                                                Texts.remove_alert_discard.name : Texts.remove_alert_discard.value,
                                                                Texts.remove_alert_msg.name : Texts.remove_alert_msg.value,
                                                                Texts.media_view_no_media.name : Texts.media_view_no_media.value,
                                                                }),

        }

    @property
    def log_path(self) -> Path:
        return self.__log_path
    
    @property
    def root_path(self) -> Path:
        return self.__root_path
    
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

