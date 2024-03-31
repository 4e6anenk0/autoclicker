import uuid

from src.clicker.core.action_factory import Action, ActionFactory


class BaseScriptNode:
    def __init__(self, action: Action, **kw):
        self.uuid = str(uuid.uuid1())
        self.name = self.__class__.__name__
        self.action = action

    def __str__(self) -> str:
       return f"Node name: [{self.name}], action: [{self.action}]. \n"

    def get_data(self):
        value = getattr(self, 'data', None)
        if value:
            return value
        
    def apply(self, action_factory: ActionFactory):
        pass