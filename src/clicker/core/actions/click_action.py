from functools import singledispatchmethod
import time
from typing import Literal, Tuple
from .base_action import BaseAction
from pynput.mouse import Controller, Button

class ClickAction(BaseAction):
    def __init__(self, controller: Controller):
        super().__init__()
        self.__controller = controller

    def execute(self, x: int = 0, y: int = 0, button: Literal['left', 'right'] = 'left', move: bool = False, count: int = 1, **kwargs):
        if move == True:
            self.move_cursor_to(x, y, self.__controller)
        else:
            self.__controller.position = (x, y)
        self.__controller.click(button=Button.left if button == 'left' else Button.right, count=count)


    def move_cursor_to(self, target_x, target_y, controller: Controller, speed=0.1):
        
        current_x, current_y = controller.position
        distance_x = target_x - current_x
        distance_y = target_y - current_y
        #steps = max(abs(distance_x), abs(distance_y)) // speed
        distance = ((distance_x ** 2) + (distance_y ** 2)) ** 0.5  # визначення загальної відстані
        steps = int(distance / speed) + 1  # визначення кількості кроків
        
        if steps == 0:
            controller.position = (target_x, target_y)
            return
        
        delta_x = distance_x / steps
        delta_y = distance_y / steps
        
        for _ in range(steps):
            current_x += delta_x
            current_y += delta_y
            controller.position = (int(current_x), int(current_y))



        
        
            

           


    