from typing import Literal
from src.clicker.models.nodes.click_node import ClickNode
from src.clicker.models.nodes.template_click_node import TemplateClickNode

NodeName = Literal['TemplateClickNode', 'ClickNode']

class NodeFactory:

    @classmethod
    def create_node(cls, node_name: NodeName, img_source: str = None, uuid: str = None):
        print(f"Node name is: {node_name}")
        match node_name:
            case 'TemplateClickNode':
                return TemplateClickNode(img_source=img_source, uuid=uuid)
            case 'ClickNode':
                return ClickNode(uuid=uuid)
            
    @classmethod
    def copy_node(cls, node, node_name: NodeName):
        match node_name:
            case 'TemplateClickNode':
                return TemplateClickNode(img_source=node['img_source'], uuid=node['uuid'], button=node['button'], move=node['move'], count=node['count'])
            case 'ClickNode':
                return ClickNode(uuid=node['uuid'], x=node['x'], y=node['y'], button=node['button'], move=node['move'], count=node['count'])