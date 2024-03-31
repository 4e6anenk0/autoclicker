from functools import singledispatchmethod
from typing import Literal
from .base_action import BaseAction
from pynput.mouse import Controller, Button

class ClickAction(BaseAction):
    def __init__(self, controller: Controller):
        super().__init__()
        self.__controller = controller

    """ def click(self, x, y):
        raise TypeError("Invavid arguments") """

    def execute(self, x: int = 0, y: int = 0, button: Literal['left', 'right'] = 'left', move: bool = False, count: int = 1, **kwargs):
        if move:
            self.__controller.move(x, y)
        else:
            self.__controller.position = (x, y)
        self.__controller.click(button=Button.left if button == 'left' else Button.right, count=count)

"""     def execute(self, **kwars):
        self.click(**kwars) """