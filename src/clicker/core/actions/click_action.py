from functools import singledispatchmethod
import time
from typing import Literal, Tuple
from .base_action import BaseAction
from pynput.mouse import Controller, Button

class ClickAction(BaseAction):
    def __init__(self, controller: Controller):
        super().__init__()
        self.__controller = controller

    """ def click(self, x, y):
        raise TypeError("Invavid arguments") """

    def execute(self, x: int = 0, y: int = 0, button: Literal['left', 'right'] = 'left', move: bool = False, count: int = 1, **kwargs):
        if move == True:
            self.move(self.__controller, (x, y))
            #self.__controller.move(x, y)
        else:
            self.__controller.position = (x, y)
        #self.__controller.
        self.__controller.click(button=Button.left if button == 'left' else Button.right, count=count)


    def move(self, controller: Controller, destination_point: Tuple[int, int]):
        start_x, start_y = controller.position
        (target_x, target_y) = destination_point

        # Розрахунок різниці
        dx = target_x - start_x
        dy = target_y - start_y

        # Кількість кроків
        steps = 100

        # Розрахунок кроку
        step_x = dx / steps
        step_y = dy / steps

        # Переміщення курсора
        for i in range(steps):
            controller.move(start_x + step_x * i, start_y + step_y * i)
            time.sleep(0.1)

    """ def move(self, controller: Controller, destination_point: Tuple[int, int]):
        # Отримання координат
        x0, y0 = controller.position
        x1, y1 = destination_point

        dl_x = x1 - x0
        dl_y = y1 - y0

        points = []

        if dl_x > dl_y:
            coef = dl_x / dl_y
            for i in range(dl_y):
                x = x0 - i + 1 * coef
                y = y0 - i + 1
                points.append((x, y))
        else:
            coef = dl_y / dl_x
            for i in range(dl_x):
                x = x0 - i + 1
                y = y0 - i + 1 * coef
                points.append((x, y))

        for point in points:
            print(point)

        # Розрахунок координат на лінії
        #points = self.bresenham(x0, y0, x1, y1) """

        
        
            

           


    