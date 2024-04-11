from typing import Tuple, Union
import cv2
from PIL import Image, ImageGrab
import numpy as np
from src.clicker.core.action_factory import Action, ActionFactory
from src.clicker.core.actions.click_action import ClickAction
from src.clicker.models.nodes.base_node import BaseScriptNode


class TemplateClickNode(BaseScriptNode):
    def __init__(self, img_source: str = None, button: Action = 'left', move: bool = False, count: int = 1, uuid: str = None, **kw):
        super().__init__(action='click', uuid=uuid, **kw)
        self.button = button
        self.move = move
        self.count = count
        self.img_source = img_source
    
    def apply(self, action_factory: ActionFactory):
        click_action: ClickAction = action_factory.get_action(action=self.action)
        (x, y) = self.get_coordinates()
        if x:
            print(f'MOVE {self.move}')
            click_action.execute(x=x, y=y, button=self.button, move=self.move, count=self.count)

    def get_coordinates(self) -> Union[Tuple[int, int], None]:
        template = self._load_data()
        transformed_template = self._rgba_to_rgb(template)
        return self._match_template_in_screenshot(transformed_template)

    def _load_data(self):
        template = cv2.imread(self.img_source, cv2.IMREAD_COLOR)
        return self._rgba_to_rgb(template)
    
    def _rgba_to_rgb(self, template):
        if template.shape[2] == 4:
            template = template[:, :, :3]
        return template
    
    def _match_template_in_screenshot(self, template) -> Union[Tuple[int, int], None]:
        screenshot = self._make_screenshot()
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)
        if max_val > 0.8:
            return max_loc
        return (None, None)
    

    def _make_screenshot(self) -> Image:
        """
        takes a screenshot of the users desktop
        """
        try:
            screenshot = ImageGrab.grab()
            #screenshot.save(fname)
            return screenshot
        except Exception as e:
            print('Cant create screenshot ' + str(e))