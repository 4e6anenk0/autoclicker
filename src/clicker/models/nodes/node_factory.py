from typing import Literal, NewType
from src.clicker.models.nodes.click_node import ClickNode
from src.clicker.models.nodes.template_click_node import TemplateClickNode


NodeName = Literal['TemplateClickNode', 'ClickNode']

class NodeFactory:

    @classmethod
    def create_node(cls, node_name: NodeName, img_source: str = None):
        print(f"Node name is: {node_name}")
        match node_name:
            case 'TemplateClickNode':
                return TemplateClickNode(img_source=img_source)
            case 'ClickNode':
                return ClickNode()