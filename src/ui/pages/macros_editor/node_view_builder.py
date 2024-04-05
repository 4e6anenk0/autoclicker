from typing import Any

from src.clicker.models.nodes.node_factory import NodeName
from src.clicker.models.nodes.base_node import BaseScriptNode
from src.ui.pages.macros_editor.node_views.node_views import ClickNodeView, TemplateClickNodeView
from src.ui.pages.macros_editor.node_view_manager import NodeViewManager


class NodeViewBuilder:
    """
    Простий допоміжний клас, який дозволяє створювати вузуальні об'єкти вузлів скрипту
    """
    def __init__(self, manager: NodeViewManager):
        self.manager = manager
        
    def get_view(self, master: Any, node: BaseScriptNode):
        node_name: NodeName = node.name
        match node_name:
            case 'ClickNode':
                return ClickNodeView(master, self.manager, node, node.get_data())
            case 'TemplateClickNode':
                return TemplateClickNodeView(master, self.manager, node, node.get_data())






        