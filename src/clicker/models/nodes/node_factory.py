from typing import Literal, NewType
from src.clicker.models.nodes.click_node import ClickNode
from src.clicker.models.nodes.template_click_node import TemplateClickNode


NodeName = Literal['TemplateClickNode', 'ClickNode']

class NodeFactory:

    @classmethod
    def create_node(cls, node_name: NodeName, data: str = None):
        print(f"Node name is: {node_name}")
        match node_name:
            case 'TemplateClickNode':
                print('TemplateClickNode will be create')
                return TemplateClickNode(data=data)
            case 'ClickNode':
                return ClickNode()