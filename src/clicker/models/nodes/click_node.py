from src.clicker.core.actions.click_action import ClickAction
from src.clicker.core.actions.base_action import BaseAction
from src.clicker.core.action_factory import Action, ActionFactory
from src.clicker.models.nodes.base_node import BaseScriptNode


class ClickNode(BaseScriptNode):
    def __init__(self, x: int = 0, y: int = 0, button: Action = 'left', move: bool = False, count: int = 1, uuid: str = None, **kw):
        super().__init__(action='click', uuid=uuid, **kw)
        self.x = x
        self.y = y
        self.button = button
        self.move = move
        self.count = count
        

    def apply(self, action_factory: ActionFactory):
        """ click_action = action_factory.get_action(action=self.action)
        click_action.execute(vars(self)) # передати властивості вузла у вигляді словаря на обробку action """
        click_action: ClickAction = action_factory.get_action(action=self.action)
        click_action.execute(x=self.x, y=self.y, button=self.button, move=self.move, count=self.count)