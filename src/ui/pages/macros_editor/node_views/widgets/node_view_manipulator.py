from typing import Any, Callable
from customtkinter import CTkFrame, CTkImage, CTkButton

from src.clicker.models.nodes.base_node import BaseScriptNode
from src.settings.settings import get_settings
from src.utils.file_helper.file_helper import load_img

class NodeViewManipulator(CTkFrame):
    def __init__(self, master: Any, node: BaseScriptNode, up_callback: Callable, down_callback: Callable, remove_callback: Callable, **kwargs):
        super().__init__(master, **kwargs)
        self.node = node
        self.up_callback = up_callback
        self.down_callback = down_callback
        self.remove_callback = remove_callback

        self.create_content().pack_configure(fill='both', expand=True)
    
    def create_content(self) -> CTkFrame:
        self.frame = CTkFrame(self)

        trash_img = load_img(get_settings().root_path.joinpath('src/icons/delete-trash.png'), resize=(40, 40))
        ctk_trash_img = CTkImage(trash_img)

        lift_up_node_button = CTkButton(self.frame, height=30, width=50, text='<', fg_color='transparent', command=lambda: self.up_callback(self.node.uuid))
        lift_down_node_button = CTkButton(self.frame, height=30, width=50, text='>', fg_color='transparent', command=lambda: self.down_callback(self.node.uuid))
        remove_button = CTkButton(self.frame, width=50, height=50, fg_color='red', image=ctk_trash_img, text='', command=lambda: self.remove_callback())    
        
        lift_up_node_button.pack_configure()
        remove_button.pack_configure(expand=True)
        lift_down_node_button.pack_configure()

        self.frame.grid_configure(row=0, column=2, sticky='nes', padx=(20, 0))

        return self.frame