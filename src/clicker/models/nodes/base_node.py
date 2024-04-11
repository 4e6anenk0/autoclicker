from typing import Dict, Union
import uuid as setid

from src.clicker.core.action_factory import Action, ActionFactory


class BaseScriptNode:
    def __init__(self, action: Action, uuid: str = None, **kw):
        self.uuid = str(setid.uuid1()) if not uuid else uuid
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
       return f"Node name: [{self.name}], action: [{self.action}], id: [{self.uuid}]. Data: \n {vars(self)} \n"

    def get_img_source(self) -> Union[str, None]:
        value = getattr(self, 'img_source', None)
        return value
        
    def apply(self, action_factory: ActionFactory):
        pass