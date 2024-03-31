from datetime import date
import json
from pathlib import Path
from uuid import UUID, uuid1
from copy import copy

from src.clicker.models.nodes.base_node import BaseScriptNode
from src.utils import create_destination_path, create_destination_dir
from .script import Script
from .macros_metadata import MacrosMetadata


class Macros:
    """
    Макрос - це сукупне представлення скрипту, разом з метаданними та інфраструктурою для керування скриптом.
    """
    def __init__(self, workdir: Path, name: str = 'new_macros', script: Script = None, uuid: UUID = None):
        """
        Конструктор макросу

        Args:
            workdir (Path): робоча директорія з усіма скриптами
            name (str, optional): ім'я макросу для відображення та у імені директорії макросу. Defaults to 'new_macros'.
            script (Script, optional): об'єкт скрипту, якщо є. Defaults to None.
            uuid (UUID, optional): ідентифікатор макросу. Якщо відсутній, то створиться новий. Defaults to None.
        """
        self.__workdir = workdir
        self.__macros_path = None
        self.__script = script
        self.__uuid = uuid1() if uuid == None else uuid
        self.__name = name
        self.__metadata: MacrosMetadata = None

    def __str__(self) -> str:
        return f"Macros: UUID - [{self.__uuid}], name - [{self.__name}] \n"

    @property
    def script(self):
        return self.__script
    
    @property
    def name(self) -> str:
        return self.__name
    
    @property
    def uuid(self) -> str:
        return str(self.__uuid)
    
    @property
    def metadata(self):
        return copy(self.__metadata)
        
    def add_script(self, script: Script):
        self.__script = script

    def save(self):
        """
        Метод для збереження макросу в директорію локального збереження макросів.

        Цей метод сворює необхідні шляхи, директорії, файли для збереження даних макросу.
        Також він зберігає метадані у полі `self.__metadata` які потім груперуються в файлі `metadata.json`
        """
        dirname = f"{date.today()}_{self.__name}"
        macros_path = self.__workdir.joinpath(dirname)
        self.__macros_path = macros_path
        create_destination_dir(macros_path.joinpath('data/'))
        script_path = macros_path.joinpath('script.json')
        self.__script.save_script_to_file(script_path)
        data = self.__script.get_data()
        global_metadata_path = macros_path.parent.joinpath('metadata.json')
        create_destination_path(global_metadata_path)
        
        self.__metadata = MacrosMetadata(uuid=str(self.uuid),
                                         name=self.__name, 
                                         macros_dir_path=str(macros_path), 
                                         script_path=str(script_path), 
                                         metadata_path=str(macros_path.joinpath('metadata.json')), 
                                         data=data)
        
        self.save_macros_metadata()
        
    def save_macros_metadata(self):
        json_to_save = json.dumps(self.__metadata.to_dict(), indent=4)
        
        with open(Path(self.__macros_path, 'metadata.json'), mode='w') as file:
            file.write(json_to_save)

    def run(self):
        """
        Запускає метод `run()` в Script
        """
        self.script.run()

    def get_node_by_uuid(self, uuid: str) -> BaseScriptNode:
        """
        Отримати вузол скрипту за вказаним uuid

        Args:
            uuid (str): строкове представлення ідентифікатору вузлу

        Returns:
            BaseScriptNode: об'єкт вузлу
        """
        return self.__script.get_node_by_uuid(uuid)[0]