from copy import copy
from datetime import date
import io
from typing import Literal, NewType, Dict, Tuple, Union
import json as _json
from uuid import UUID

from src.clicker.models.nodes import BaseScriptNode, NodeFactory
from src.utils import AppLogger

logger = AppLogger.get_logger(__name__)

NodePosition = NewType('NodePosition', int)

class Script:
    """
    Клас для реалізації логіки скрипта.
    """
    def __init__(self):
        self.__nodal_view: list[BaseScriptNode] = []

    def __str__(self) -> str:
        buffer = io.StringIO()
        for node in self.__nodal_view:
            buffer.write(str(node))
        return buffer.getvalue()

    def __repr__(self) -> str:
        buffer = io.StringIO()
        for node in self.__nodal_view:
            buffer.write(str(vars(node)))
        return buffer.getvalue()

    @classmethod
    def from_nodes(cls, nodes: list[BaseScriptNode]):
        """
        Конструктор для створення об'єкта скрипту з вказаного списку вузлів.

        Args:
            nodes (list[BaseScriptNode]): список вузлів для створення скрипту

        Returns:
            _type_: об'єкт скрипту
        """
        obj = cls()
        obj.add_nodes(nodes)
        return obj

    @classmethod
    def from_file(cls, path_to_file: str):
        """
        Конструктор для створення об'єкта скрипту з існуючого `.js` файлу

        Args:
            path_to_file (str): шлях до файлу зі скриптом

        Returns:
            Script: створений об'єкт скрипту
        """
        obj = cls()
        obj.load_script_from_file(path_to_file)
        return obj

    def run(self):
        """
        Метод який запускає скрипт
        """
        for node in self.__nodal_view:
            pass

    def insert_node(self, node: BaseScriptNode, index: Union[NodePosition, int], order: Literal['before', 'after']):
        """
        Вставити вузол в зазначену позицію відповідно індексу розміщення іншого вузла

        Args:
            node (BaseScriptNode): вузол якій потрібно додати до інших вузлів
            index (Union[NodePosition, int]): індекс вузла відповідно котрого треба робити розміщення
            order (Literal["before", "after"]): розміщення відповідно індекса вузла, який вказаний вище

        Raises:
            ValueError: Слід передати правильне значення `order`, інакше буде помилка
        """
        if order == 'before':
            self.__nodal_view.insert(index, node)
        elif order == 'after':
            self.__nodal_view.insert(index + 1, node)
        else:
            raise ValueError(f"An incorrect value was passed: ID - [{index}], position - [{order}].")
        
    def add_node(self, node: BaseScriptNode):
        """
        Додати вузол до скрипту. Додає вузол в кінець списку

        Args:
            node (BaseScriptNode): вузол який слід додати
        """
        self.__nodal_view.append(node)

    def add_nodes(self, nodes: list[BaseScriptNode]):
        """
        Додати список вузлів до скрипту

        Args:
            nodes (list[BaseScriptNode]): список вузлів
        """
        self.__nodal_view.extend(nodes)

    def save_script_to_file(self, path_to_file: str):
        """
        Зберегти скрипт до файлу вказаного за шлязом `path_to_file`. Файл має існувати заздалегіть

        Args:
            path_to_file (str): шлях до існуючого файлу
        """
        script = {'script' : []}
        for node in self.__nodal_view:
            script['script'].append(vars(node)) # vars(node) перетворює вузол тупу BaseScriptNode в Dict
        json_obj = _json.dumps(script, indent=4)
        with open(file=path_to_file, mode='w') as file: 
            file.write(json_obj)

    def load_script_from_file(self, path_to_file: str):
        """
        Завантажити скрипт з файлу. Файл скрипту повинен існувати

        Args:
            path_to_file (str): шлях до файлу з скриптом
        """
        with open(file=path_to_file) as file: 
            json_obj = _json.load(file)
        for node in json_obj["script"]:
            self.add_node(NodeFactory.create_node(node['name'], node))

    def get_node_by_uuid(self, uuid: str) -> Tuple[BaseScriptNode, NodePosition]:
        """
        Отримати вузол скрипту за вказаним ідентифікатором `uuid`

        Args:
            uuid (str): ідентифікатор вузла у строковому представленні

        Returns:
            Tuple[BaseScriptNode, NodePosition]: повертає кортеж зі значенням вузол та його індекс розміщення в списку
        """
        index = 0
        for node in self.__nodal_view:
            if node.uuid == uuid:
                return (node, index)
            index += 1
            
    def lift_down_node_order(self, node_uuid: str):
        """
        Змістити вузол зі вказаним `uuid` збільшивши значення на одну позицію відносно поточного індексу в списку.
        Тобто, це розмістить вузол нижче у порядку виклику. Якщо `node_uuid` відповідає останьому вузлу в списку,
        то фунуція виконається без внесення жодних змін

        Args:
            node_uuid (str): ідентифікатор вузла у строковому представленні
        """
        (node, index) = self.get_node_by_uuid(node_uuid)
        if len(self.__nodal_view) == index + 1:
            return
        self.__nodal_view.remove(node)
        self.insert_node(node, index, order='after')

    def lift_up_node_order(self, node_uuid: str):
        """
        Змістити вузол зі вказаним `uuid` зменшивши значення на одну позицію відносно поточного індексу в списку.
        Тобто, це розмістить вузол вище у порядку виклику.

        Args:
            node_uuid (str): ідентифікатор вузла у строковому представленні
        """
        (node, index) = self.get_node_by_uuid(node_uuid)
        self.__nodal_view.remove(node)
        self.insert_node(node, index, order='before')

    def change_node_order(self, node_uuid: str, new_index: Union[NodePosition, int]):
        """
        Метод що дозволяє змінити положення вуза в списку за довільним значенням індексу нового розміщення.

        Args:
            node_uuid (str): ідентифікатор вузла у строковому представленні
            new_index (Union[NodePosition, int]): нове розміщення вузлу

        Raises:
            ValueError: неможливо вказати індекс що `>=` ніж останній максимальний індекс у списку
        """
        if new_index >= len(self.__nodal_view):
            logger.error("The index value cannot be greater than the maximum index in the node list.")
            raise ValueError("The index value cannot be greater than the maximum index in the node list.")
        (node, _) = self.get_node_by_uuid(node_uuid)
        self.__nodal_view.remove(node)
        self.insert_node(node, new_index, order='before')

    def get_data(self) -> Dict[str, str]:
        """
        Метод який дозволяє отримати усі шляхи до шаблонів з прив'язкою до ідентифікатора вузла, якому належить цей шаблон.
        
        Цей метод використовується для групування усіх необхідних шляхів до даних потрібних для вузлів, щоб потім зручно завантажувати
        ці данні в вузли з відповідного файду метаданних.

        Returns:
            Dict[str, str]: де Dict[(1), (2)] - 1. ідентифікатор вузла, 2. шлях до шаблону (якщо у вузла є `data`)
        """
        data_collect = {}
        for node in self.__nodal_view:
            data = node.get_data()
            if data:
                data_collect[str(node.uuid)] = data
        return data_collect
    
    def get_nodes(self) -> list[BaseScriptNode]:
        """
        Дозволяє отримати копію списку вузлів які містяться в скрипті.

        Returns:
            list[BaseScriptNode]: копія списку вузлів
        """
        return copy(self.__nodal_view) 

 




