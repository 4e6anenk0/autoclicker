from pathlib import Path
import json
import shutil
from typing import Any, Dict, Generator, Tuple, Union
from uuid import UUID

from src.clicker.models.macros_metadata import MacrosMetadata
from src.clicker.models.script import Script
from src.clicker.models.macros import Macros
from src.utils.logger.logger import AppLogger

logger = AppLogger.get_logger(__name__)

class MacrosManager:
    """
    Це клас для керування усіма макросами. Збереження, отримання, запуск та оновлення макросів відбувається з цього класу.
    """
    def __init__(self, workdir: str, path_to_metadata: str):
        """
        Конструктор для менеджера макросів

        Args:
            workdir (str): робоча директорія з розміщенням усіх макросів доступних для цього менеджера
            path_to_metadata (str): шлях до файлу метаданих
        """
        self.__workdir = workdir
        self.__metadata_filename = 'metadata.json'
        self.__path_to_metadata: Path = Path(path_to_metadata)
        self.__metadata: Dict[str, MacrosMetadata] = {} # завантажені глобальні метадані
        self.__macroses: Dict[str, Macros] = {} # завантажені макроси

        self.__is_loaded_metadata: bool = False
        

    @property
    def workdir(self):
        return self.__workdir

    ### Робота з макросами індивідуально: ------------------------------------------------------------

    def add_macros(self, macros: Macros) -> bool:
        """
        Додати макрос до поточного списку макросів

        Args:
            macros (Macros): макрос якій треба додати
        """
        
        self.__macroses[macros.uuid] = macros
        if macros.metadata:
            self.__metadata[macros.uuid] = macros.metadata
        return True

    def remove_macros(self, uuid: str, localy: bool = False) -> bool:
        """
        Видалити макрос зі списку макросів.

        Args:
            uuid (str): ідентифікатор макросу.
            localy (bool, optional): Чи видаляти макрос локально. За замовчанням, видаляє лише з кешу. Defaults to False.

        Returns:
            bool: True - якщо видалення успішне, False - якщо видалення зазнало невдачі.

        Для деталей помилок, які виникають, треба читати лог.
        """
        try:
            if localy and self.__macroses[uuid]:
                if self.__metadata[uuid]:
                    shutil.rmtree(self.__metadata[uuid].macros_dir_path)
                else:
                    logger.warning(f"__macroses[uuid].metadata is None: {e}")
            self.__macroses.pop(uuid)
            self.__metadata.pop(uuid)
            return True
        except KeyError as e:
            logger.error(f"Maybe you passed a value for a key that doesn't exist. KeyError: {e}")
            return False
        except Exception as e:
            logger.exception(f"{e}")
            return False

    def load_macros_by_metadata(self, metadata: MacrosMetadata) -> Tuple[Union[Macros, None], bool]:
        """
        Завнтажити макрос через метадані конкретного макросу

        Args:
            metadata (MacrosMetadata): метадані макросу який слід завантажити
        
        Returns:
            bool: чи вдалося завантажити макрос через метадані
        """
        try:
            script = Script()
            script.load_script_from_file(metadata.script_path)
            loaded_macros = Macros(self.__workdir, metadata.name, script, metadata.uuid)
            self.__macroses[metadata.uuid] = loaded_macros
            return loaded_macros, True
        except Exception as e:
            logger.exception(f'{e}')
            return None, False

    def load_macros_by_metadata_file(self, metadata_file_path: str) -> Tuple[Union[Macros, None], bool]:
        """
        Завантажити макрос через передачу шляху до файлу локальних метаданих

        Args:
            metadata_file_path (str): шлях до локальних метаданих

        Returns:
            bool: чи вдалося завантажити макрос через шлях до файлу локальних метаданих
        """
        try:
            metadata = self.load_metadata(path_to_file=metadata_file_path)
            if metadata:
                script = Script()
                script.load_script_from_file(metadata['script_path'])

                macros = Macros(workdir=self.__workdir, 
                                name=metadata['name'], 
                                script=script, 
                                uuid=UUID(metadata['uuid']))
                self.__macroses[metadata['uuid']] = macros
            return macros, True
        except Exception as e:
            logger.exception(f'{e}')
            return None, False
            
    def get_macros_by_uuid(self, uuid: str) -> Macros:
        """
        Отримати макрос за вказаним ідентифікатором

        Args:
            uuid (str): строковий ідентифікатор макросу

        Returns:
            Macros: об'єкт макросу
        """
        return self.__macroses.get(uuid)
    
    def save_macros_by_uuid(self, uuid: str) -> bool:
        """
        Зберегти мкрос з вказаним `uuid` ідентифікатором

        Args:
            uuid (str): ідентифікатор макросу

        Returns:
            bool: чи вдалося зберегти макрос
        """
        try:
            self.__macroses[uuid].save()
            return True
        except Exception as e:
            logger.exception(f'{e}')
            return False

    def save_local_metadata(self, macros_uuid: str) -> bool:
        """
        Зберегти локальні метадані для макросу

        Args:
            macros_uuid (str): ідентифікатор макросу

        Returns:
            bool: чи вдалося зберегти метадані макросу локально
        """
        try:
            self.__macroses.get(macros_uuid).save_macros_metadata()
            return True
        except Exception as e:
            logger.exception(f'{e}')
            return False

    ### Робота з усіма макросами: --------------------------------------------------------------------

    def load_all_macroses(self) -> bool:
        """
        Завантажити всі макроси, що вказані у глобальному файлі `metadata.json`

        Returns:
            bool: чи вдалося завантажити усі макроси
        """
        try:
            if self.__is_loaded_metadata:
                for uuid, metadata in self.__metadata.items():
                    script = Script()
                    script.load_script_from_file(metadata.script_path)
                    self.__macroses[uuid] = Macros(workdir=self.__workdir, name=metadata.name, script=script, uuid=UUID(uuid))
            return True
        except Exception as e:
            logger.exception(f'{e}')
            return False
    
    def load_macroses(self, batch_size: int) -> Union[Generator[list[Macros], Any, None]]:
        metadatas: list[MacrosMetadata] = list(self.__metadata.values())
        
        
        for i in range(0, len(metadatas), batch_size):
            batch = []
            for metadata in metadatas[i:i + batch_size]:
                data = self.load_macros_by_metadata_file(metadata.metadata_path)[0]
                self.__macroses[data.uuid] = data
                if data:
                    batch.append(data)
            yield batch
        #batch = []
    
    def get_macroses_by_filter():
        pass

    def get_all_macroses(self) -> list[Macros]:
        """
        Отримати список усіх макросів

        Returns:
            list[Macros]: список доступних макросів
        """
        return self.__macroses.values()
    
    def save_all_macroses(self) -> bool:
        """
        Зберігає усі макроси через виклик методу `save()` в кожному макросі, та зберігає відповідні метадані,
        що містяться у поточному списку макросів у глобальний файл `metadata.json`

        Returns:
            bool: чи вдалося зберегти усі макроси
        """
        try:
            for macros in self.__macroses.values():
                macros.save()
           
            self.save_global_metadata()
            return True
        except Exception as e:
            logger.exception(f'{e}')
            return False

    def save_global_metadata(self) -> bool:
        """
        Зберігає глобальні або спільні метадані для усіх макросів

        Returns:
            bool: чи вдалося зберегти спільні метаданні
        """
        try:
            data = {}
            for uuid, macros in self.__macroses.items():
                if macros.metadata:
                    data[uuid] = macros.metadata.to_dict()

            json_to_save = json.dumps(data, indent=4)
            
            with open(Path(self.__workdir, self.__metadata_filename), mode='w') as file:
                file.write(json_to_save)
            return True
        except Exception as e:
            logger.exception(f'{e}')
            return False

    def update_global_metadata(self):
        """
        Оновлює значення метаданих менеджеру про методані макросів, які завантажені в нього
        """
        for macros in self.__macroses.values():
            if macros.metadata:
                self.__metadata[macros.uuid] = macros.metadata
    
    def load_global_metadata(self):
        """
        Завантажити спільні (глобальні) метадані

        Returns:
            bool: чи вдалося завантажити дані
        """
        datas = self.load_metadata(self.__path_to_metadata)

        if datas:
            for uuid, data in datas.items():
                self.__metadata[uuid] = MacrosMetadata(uuid=data['uuid'], 
                                             date=data['date'], 
                                             name=data['name'], 
                                             macros_dir_path=data['macros_dir_path'],
                                             script_path=data['script_path'],
                                             metadata_path=data['metadata_path'],
                                             img_sources=data['img_sources'])

            self.__is_loaded_metadata = True


    def load_metadata(self, path_to_file: str) -> Union[Dict[str, Any], None]:
        """
        Допоміжний метод для завантаження метаданих з файлу

        Args:
            path_to_file (str): шлях до файлу з метаданими

        Returns:
            Union[Dict[str, Any], None]: Dict представлення метаданих
        """
        path = Path(path_to_file)
        if path.is_file() and path.suffix == '.json':
            with open(file=path) as file:
                try:
                    json_obj = json.load(file)
                    return json_obj
                except Exception as e:
                    logger.exception(f"Failed to load data from file. Maybe the file [{path}] has no data.", exc_info=False)
                    return None
            
            
