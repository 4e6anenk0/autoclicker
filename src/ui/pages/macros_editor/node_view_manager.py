from typing import Dict
from src.clicker.models.nodes.base_node import BaseScriptNode
from src.clicker.models.script import Script
from src.ui.pages.macros_editor.node_views.node_view import NodeView


class NodeViewManager:
    def __init__(self, script: Script):
        self.script = script
        self.editing_nodes: Dict[str, BaseScriptNode] = {}
        self.editing_node_views: list[NodeView] = [] 
    
    def add_node(self, node: BaseScriptNode):
        """
        Додавання вузлу скрипту до пов'язаного скрипту

        Args:
            node (BaseScriptNode): вузол скрипту
        """
        self.script.add_node(node)

    def editing_nodes_to_script(self):
        self.script.add_nodes(self.editing_nodes.values())

    def synchronize_data_from_view(self):
        for node in self.editing_node_views:
            node.update_node()
    
    def remove_node(self, node_id: str):
        """
        Видаляємо вузол зі списку як графічного представлення так і з самого скрипту

        Args:
            node_id (str): UUID вузлу у сроковому представленні
        """
        self.editing_nodes.pop(node_id)
        for node_view in self.editing_node_views:
            if node_view.node_id == node_id:
                self.editing_node_views.remove(node_view)
        self.script.remove_node_by_uuid(node_id)

    def clear_all(self):
        """
        Дозволяє очистити `NodeViewManager`
        """
        self.editing_nodes.clear()
        for node_view in self.editing_node_views:
            node_view.destroy()
        self.editing_node_views.clear()
        self.script = Script()
    
    def lift_up_node(self, node_id: str):
        """
        Підняти вузол у візуальному поданні списку вузлів

        Args:
            node_id (str): UUID вузла, у строковому представленні, який треба підняти
        """
        (old_position, new_position) = self.script.lift_up_node_order(node_id) # змінюємо позицію в скрипті та отримуємо значення позицій
        if old_position == new_position: # жодних змін коли позиція не змінна
            return
        # NodeView з індексом старої позиції розміщуємо перед вузлом який займає цільову позицію
        # це вносить зміни лише візуально, потім треба зробити фактичні зміни в списку
        self.editing_node_views[old_position].pack_configure(before=self.editing_node_views[new_position])
        
        # робимо зміни в списку візуального представлення вузлів, щоб закріпити зміни фактично
        old = self.editing_node_views[old_position]
        self.editing_node_views.insert(new_position, old)
        self.editing_node_views.pop(old_position + 1)

    def lift_down_node(self, node_id: str):
        """
        Опустити вузол у візуальному поданні списку вузлів

        Args:
            node_id (str): UUID вузла, у строковому представленні, який треба опустити
        """
        (old_position, new_position) = self.script.lift_down_node_order(node_id)
        if old_position == new_position:
            return
        self.editing_node_views[old_position].pack_configure(after=self.editing_node_views[new_position])
        
        old = self.editing_node_views[old_position]
        self.editing_node_views.insert(new_position + 1, old)
        self.editing_node_views.pop(old_position)