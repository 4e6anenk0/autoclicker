from typing import Any, Callable, Tuple
from customtkinter import CTkFrame, CTkToplevel
from PIL.Image import Image

from src.clicker.models.nodes.base_node import BaseScriptNode
from src.clicker.models.nodes.click_node import ClickNode
from src.ui.widgets.alert import Alert
from src.ui.pages.macros_editor.node_views.widgets.media_view import MediaView
from src.ui.pages.macros_editor.node_views.widgets.node_view_manipulator import NodeViewManipulator
from src.utils.file_helper.file_helper import save_img


class NodeView(CTkFrame):
    def __init__(self, master: Any, manager: Any, node: BaseScriptNode, path_to_img: str = None, is_selectable: bool = False, **kwargs):
        super().__init__(master, **kwargs)
        self.manager = manager
        self.node = node
        self.node_id = node.uuid
        self.alert: CTkToplevel = None
        self.path_to_img = path_to_img
        self.is_selectable = is_selectable
        self.img: Image = None
        self.rimg: Image = None

        self.frame = CTkFrame(self)
        self.frame.grid_columnconfigure([1], weight=1)

        self.build_media_view()
        self.build_manipulator_view()

    def remove_alert(self):
        self.alert.destroy()
        self.alert = None
    
    def show_remove_alert(self):
        if self.alert is None or not self.alert.winfo_exists():
            self.alert = Alert(callback_confirm=self.remove_node, callback_discard=self.remove_alert, confirm_btn_text='Так', discard_btn_text='Ні', msg='Чи хочете ви видалити вузол?')
        else:
            self.alert.focus()

    """ def save_image(self, path: str):
        if self.img:
            self.path_to_img = f"{path}{self.node_id}"
            save_img(self.img, path=self.path, name=f"{self.node_id}") """
            #save_img(self.img, path=self.path, name=f"{self.node_id}_rsize")
    
    def remove_node(self):
        self.manager.remove_node(self.node.uuid)
        self.alert.destroy()
        self.alert = None
        self.destroy()

    def build_media_view(self):
        self.media_view = MediaView(self.frame, path_to_img=self.path_to_img, is_selectable=self.is_selectable, node_view=self)
        self.media_view.grid_configure(row=0, column=0, sticky='nws')

    def build_manipulator_view(self):
        self.manipulator_view = NodeViewManipulator(self.frame, self.node, self.manager.lift_up_node, self.manager.lift_down_node, self.show_remove_alert)
        self.manipulator_view.grid_configure(row=0, column=2, sticky='nes', padx=(20, 0))

    def update_node(self):
        pass

    def save_img_data(self, path: str):
        if self.img:
            save_img(self.img, path=path, name=self.node_id)