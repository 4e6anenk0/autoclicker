import uuid

from src.clicker.core.action_factory import Action, ActionFactory


class BaseScriptNode:
    def __init__(self, action: Action, **kw):
        self.uuid = str(uuid.uuid1())
        self.name = self.__class__.__name__
        self.action = action

    def __eq__(self, __value: object) -> bool:
        if __value is None:
            return False
        if isinstance(__value, BaseScriptNode):
            return self.uuid == __value.uuid
        return False
    
    def __ne__(self, __value: object) -> bool:
        return not self.__eq__(__value)
    
    def __hash__(self):
        return hash(self.uuid)
    
    def __str__(self) -> str:
       return f"Node name: [{self.name}], action: [{self.action}]. \n"

    def get_data(self):
        value = getattr(self, 'data', None)
        if value:
            return value
        
    def apply(self, action_factory: ActionFactory):
        pass