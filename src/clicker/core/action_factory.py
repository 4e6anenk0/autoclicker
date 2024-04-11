from enum import Enum
from typing import Annotated, Callable, Dict, Generic, Literal, NewType, Set, TypeVar, Union
from pynput.mouse import Controller as MouseController
from pynput.keyboard import Controller as KeyboardController

from src.clicker.core.actions.click_action import ClickAction
from src.clicker.core.actions.base_action import BaseAction

Action = Literal['click', 'scroll']

""" class ActionController:
    def __init__(self):
        self.__mouse_controller = MouseController()
        self.__keyboard_controller = KeyboardController()
        self.__actions: Dict[str, BaseAction] = {}

    def add_action(self, action: Action):
        match action:
            case 'click':
                self.__actions['click'] = ClickAction() """



class ActionFactory:
    def __init__(self):
        self.__actions: Dict[str, BaseAction] = {}
        self.__mouse_controller = MouseController()
        self.__keyboard_controller = KeyboardController()
    
    def create_action(self, action: Action):
        match action:
            case 'click':
                self.__actions['click'] = ClickAction(controller=self.__mouse_controller)
    
    def get_action(self, action: Action) -> Union[BaseAction , None]:
        self.create_action(action)
        return self.__actions.get(action)
        """ if action in self.__actions:
            return self.__actions[action]
        else:
            self.create_action(action)
            return self.__actions.get(action) """
    

