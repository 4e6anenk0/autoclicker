from pathlib import Path
from typing import Any
from customtkinter import CTkFrame, CTkLabel, CTkEntry, CTkComboBox, CTkCheckBox, CTkToplevel

from src.clicker.models.nodes.template_click_node import TemplateClickNode
from src.clicker.models.nodes.base_node import BaseScriptNode
from src.clicker.models.nodes.click_node import ClickNode
from src.ui.widgets.alert import Alert
from src.ui.pages.macros_editor.node_view_manager import NodeViewManager
from src.ui.pages.macros_editor.node_views.node_view import NodeView
from src.ui.pages.macros_editor.node_views.widgets.media_view import MediaView
from src.ui.pages.macros_editor.node_views.widgets.node_view_manipulator import NodeViewManipulator
from src.utils.file_helper.file_helper import save_img




class ClickNodeView(NodeView):
    def __init__(self, master: Any, manager: Any, node: ClickNode = None, path_to_img: str = None, **kwargs):
        super().__init__(master, manager, node, path_to_img, **kwargs)
        self.node = node
        self.create_content().pack_configure(fill='both', expand=True)

    def create_content(self):
        #self.frame = CTkFrame(self, fg_color='transparent', bg_color='transparent')

        data_view = CTkFrame(self.frame, fg_color="transparent")

        row_1 = CTkFrame(data_view, fg_color="transparent")
        info = CTkLabel(row_1, text=f'Node: {self.node.name}', anchor='w')
        info.pack_configure(fill='both', expand=True)
        row_1.pack_configure(fill='x', expand=False, padx=5, pady=(10, 5))

        row_2 = CTkFrame(data_view, fg_color="transparent")
        row_2.grid_columnconfigure([1,3], weight=1, minsize=100)
        x_label = CTkLabel(row_2, text='X:', anchor='w')
        x_label.grid_configure(row=0, column=0, sticky='w', padx=(0, 10))
        self.x_input = CTkEntry(row_2)
        self.x_input.grid_configure(row=0, column=1, sticky='we', padx=(0, 10))
        y_label = CTkLabel(row_2, text='Y:', anchor='w')
        y_label.grid_configure(row=0, column=2, sticky='w', padx=(0, 10))
        self.y_input = CTkEntry(row_2)
        self.y_input.grid_configure(row=0, column=3, sticky='we', padx=(0, 10))
        row_2.pack_configure(fill='x', expand=False, padx=5, pady=5)

        row_3 = CTkFrame(data_view, fg_color="transparent")
        row_3.grid_columnconfigure([1], weight=1, minsize=60)
        row_3.grid_columnconfigure([3], weight=1, minsize=40)
        button_type_label = CTkLabel(row_3, text='Клавіша миші:')
        button_type_label.grid_configure(row=0, column=0, sticky='w', padx=(0, 10))
        self.button_type = CTkComboBox(row_3, values=['left', 'right'])
        self.button_type.grid_configure(row=0, column=1, sticky='w')
        count_of_click_label = CTkLabel(row_3, text='Кліків:')
        count_of_click_label.grid_configure(row=0, column=2, sticky='w', padx=(10, 10))
        self.count_of_click = CTkEntry(row_3, width=50)
        self.count_of_click.grid_configure(row=0, column=3, sticky='w', padx=(0, 10))
        row_3.pack_configure(fill='x', expand=False, padx=5, pady=5)

        row_4 = CTkFrame(data_view, fg_color="transparent")
        use_move_label = CTkLabel(row_4, text='Показувати переміщення:')
        use_move_label.grid_configure(row=0, column=0, sticky='w')
        self.use_move = CTkCheckBox(row_4, text='')
        self.use_move.grid_configure(row=0, column=1, padx=(10, 0))
        row_4.pack_configure(fill='x', expand=True, padx=5, pady=(5, 10))

        data_view.grid_configure(row=0, column=1, sticky='nwse', pady=20)

        if self.node:
            self.fill_from_node(self.node)

        return self.frame
    
    def fill_from_node(self, node: ClickNode):
        self.node = node
        self.x_input.insert(0, str(node.x))
        self.y_input.insert(0, str(node.y))
        self.button_type.set(node.button)
        self.count_of_click.insert(0, str(node.count))
        #self.use_move.toggle(int(node.move))
        if node.move == True:
            self.use_move.select()
        else:
            self.use_move.deselect()

    def update_node(self):
        self.node.x = int(self.x_input.get())
        self.node.y = int(self.y_input.get())
        self.node.button = self.button_type.get()
        self.node.count = int(self.count_of_click.get())
        print(bool(self.use_move.get()))
        self.node.move = bool(self.use_move.get())


class TemplateClickNodeView(NodeView):
    def __init__(self, master: Any, manager: Any, node: TemplateClickNode = None, path_to_img: str = None, **kwargs):
        super().__init__(master, manager, node, path_to_img, True, **kwargs)
        self.node = node

        self.create_content().pack_configure(fill='both', expand=True)

    def create_content(self):
        #self.frame = CTkFrame(self, fg_color='transparent', bg_color='transparent')

        #self.frame.grid_columnconfigure([1], weight=1)

        data_view = CTkFrame(self.frame, fg_color="transparent")

        row_1 = CTkFrame(data_view, fg_color="transparent")
        info = CTkLabel(row_1, text=f'Node: {self.node.name}', anchor='w')
        info.pack_configure(fill='both', expand=True)
        row_1.pack_configure(fill='x', expand=False, padx=5, pady=(10, 5))

        row_2 = CTkFrame(data_view, fg_color="transparent")
        button_type_label = CTkLabel(row_2, text='Клавіша миші:')
        button_type_label.grid_configure(row=0, column=0, sticky='w', padx=(0, 10))
        self.button_type = CTkComboBox(row_2, values=['left', 'right'])
        self.button_type.grid_configure(row=0, column=1, sticky='w')
        count_of_click_label = CTkLabel(row_2, text='Кліків:')
        count_of_click_label.grid_configure(row=0, column=2, sticky='w', padx=(10, 10))
        self.count_of_click = CTkEntry(row_2, width=50)
        self.count_of_click.grid_configure(row=0, column=3, sticky='w', padx=(0, 10))
        row_2.pack_configure(fill='x', expand=False, padx=5, pady=5)

        row_3 = CTkFrame(data_view, fg_color="transparent")
        use_move_label = CTkLabel(row_3, text='Показувати переміщення:')
        use_move_label.grid_configure(row=0, column=0, sticky='w')
        self.use_move = CTkCheckBox(row_3, text='')
        self.use_move.grid_configure(row=0, column=1, padx=(10, 0))
        row_3.pack_configure(fill='x', expand=False, padx=5, pady=(5, 10))

        data_view.grid_configure(row=0, column=1, sticky='nwse', pady=20)

        if self.node:
            self.fill_from_node(self.node)

        return self.frame
    
    """ def save_callback(self, img):
        save_img(img, path=self.manager) """
    
    def fill_from_node(self, node: ClickNode):
        self.node = node
        self.button_type.set(node.button)
        self.count_of_click.insert(0, str(node.count))
        #self.use_move.toggle(int(node.move))
        if node.move == True:
            self.use_move.select()
        else:
            self.use_move.deselect()

    """ def set_path_to_img(self):
        path_to_img
        if self.path_to_img != path:
            self.path_to_img = path """

    def update_node(self):
        #self.node.img_source = self.
        self.node.button = self.button_type.get()
        self.node.count = int(self.count_of_click.get())
        self.node.move = bool(self.use_move.get())
        
        if self.manager.path_to_data:
            path_to_img = str(Path(self.manager.path_to_data).joinpath(f"{self.node_id}.png"))
            if self.node.img_source != path_to_img:
                self.node.img_source = path_to_img
