from typing import Any, Callable, Dict, Tuple
from customtkinter import *
from PIL.Image import Image
from PIL import Image as ImageFactory
from tktooltip import ToolTip

from src.clicker.models.nodes.click_node import ClickNode
from src.clicker.models.nodes.base_node import BaseScriptNode
from src.clicker.models.script import Script
from src.clicker.models.macros import Macros
from src.clicker.models.nodes.node_factory import NodeFactory, NodeName
from src.settings.settings import Settings, Texts, get_settings
from src.ui.pages.page import Page
from src.ui.widgets.alert import Alert
from src.utils.file_helper.file_helper import load_img


class MetadataInfo(CTkToplevel):
    def __init__(self, macros: Macros, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.macros = macros

        self.create_content().pack_configure(fill='both', expand=True)

    def create_content(self):
        self.frame = CTkFrame(self)

        self.scrollable_content = CTkScrollableFrame(self.frame)
        self.scrollable_content.pack_configure(fill='both', expand=True)

        header_frame = CTkFrame(self.scrollable_content)

        macros_name_title = CTkLabel(header_frame, text = f'Macros: {self.macros.name}')
        macros_id = CTkLabel(header_frame, text = f'Macros UUID: {self.macros.uuid}')
        metadata_view = CTkTextbox()
        metadata_view.insert('0.0', text=f"{str(self.macros.metadata.to_dict())}")

        macros_name_title.pack_configure(fill='x', expand=False)
        macros_id.pack_configure(fill='x', expand=False)
        metadata_view.pack_configure(fill='x', expand=False)

        header_frame.pack_configure(fill='both', expand=True)

        return self.frame


class MacrosEditor(Page):
    def __init__(self, master: Page, settings: Settings, macros: Macros = None, **kwargs):
        super().__init__(master, settings, **kwargs)
        self.macros = macros
        self.script = Script() if macros is None else macros.script
        self.editing_nodes: Dict[str, BaseScriptNode] = {}
        self.editing_node_views: list[NodeView] = []
        self.create_content().pack_configure(fill='both', expand=True)


    def create_content(self) -> CTkFrame:
        self.frame = CTkFrame(self)
        
        self.header = CTkFrame(self)
        self.header.pack_configure(fill='both', expand=False)
        
        self.scrollable_content = CTkScrollableFrame(self.frame)
        self.scrollable_content.pack(fill='both', expand=True)

        # правильні прив'язки для роботи як в linux так і в windows
        # У Windows коліщатко миші прив’язується за допомогою <MouseWheel> методу, 
        # але для машини Linux прив’язка коліщатка миші призначена <Button-4>для прокручування вгору та <Button-5>
        self.scrollable_content.bind_all("<Button-4>", lambda e: self.scrollable_content._parent_canvas.yview("scroll", -1, "units"))
        self.scrollable_content.bind_all("<Button-5>", lambda e: self.scrollable_content._parent_canvas.yview("scroll", 1, "units"))
        
        title_frame = CTkFrame(self.header, fg_color='transparent')
        title_frame.grid_columnconfigure(1, weight=1)
        
        self.title = CTkEntry(title_frame, font=CTkFont(size=20, weight='bold'), placeholder_text=get_settings().get_ui_text(Texts.macros_editor_title_placeholder), width=400)
        self.title.grid_configure(row=0, column=0, sticky='w')

        metadata_info = CTkButton(title_frame, width=100, height=42, text='info', command=self.open_metadata_info)
        metadata_info.grid_configure(row=0, column=1, sticky='w', padx=10)

        save_macros_button = CTkButton(title_frame, text=get_settings().get_ui_text(Texts.macros_editor_save_macros_button), height=42, fg_color='green')
        save_macros_button.grid_configure(row=0, column=2, sticky='e')

        title_frame.pack_configure(padx=10, pady=10, fill='x', expand=True)

        header_panel = HeaderPanel(self.header, editor=self)
        header_panel.pack_configure(anchor='w')
        
        if self.macros: # Заповнення scrollable_content або існуючими вузлами в макросі, або повідомленням їх відсутності
            for node in self.macros.get_nodes():
                node_view = NodeView(self.scrollable_content, self, path_to_img=node.get_data)

                self.editing_node_views.append(node_view)
                node_view.pack_configure(padx=(0, 10), pady=10) 
        else:
            self.no_info = CTkLabel(self.scrollable_content, text=get_settings().get_ui_text(Texts.macros_editor_no_info_label), anchor='n')
            self.no_info.pack_configure(pady=30)

        return self.frame
    
    def create_macros(self):
        self.macros = Macros()
    
    def open_metadata_info(self):
        self.metadata_info = MetadataInfo(macros=self.macros)
        self.metadata_info.focus()

    def fill_data_from_macros_if_exist(self):
        if self.macros:
            self.title.insert(index='0.0', string=self.macros.name)
    
    def save(self):
        print('Save called...')
        print(self.title.get())

    def remove_node(self, node_id: str):
        self.editing_nodes.pop(node_id)
        for node_view in self.editing_node_views:
            if node_view.node_id == node_id:
                self.editing_node_views.remove(node_view)
        self.script.remove_node_by_uuid(node_id)

    def clear_all(self):
        self.editing_nodes.clear()
        for node_view in self.editing_node_views:
            node_view.destroy()
        self.editing_node_views.clear()
        self.script = Script()
        self.macros = None
        self.no_info.pack_configure(pady=30)

    def create_node_view(self, node: BaseScriptNode):
        return NodeView(self.scrollable_content, self, node=node)
            

    def update_node_views(self):
        print(self.editing_node_views)
        for node in self.script.get_nodes():
            if node.uuid not in self.editing_nodes:
                self.editing_nodes[node.uuid] = node

                #node_view = NodeView(self.scrollable_content, self, node_id = node.uuid, path_to_img=node.get_data())
                node_view = self.create_node_view(node)
                
                self.editing_node_views.append(node_view)
                node_view.pack_configure(padx=(0, 10), pady=10)
        
    @classmethod
    def from_macros(cls, master: Page, settings: Settings, macros: Macros, **kwargs):
        macros_editor_page = cls(master, settings, **kwargs)
        nodes = macros.get_nodes()
        for node in nodes:
            pass
    
    
class HeaderPanel(CTkFrame):
    def __init__(self, master: Any, editor: MacrosEditor, **kwargs):
        super().__init__(master, **kwargs)
        self.node_names: NodeName = ['TemplateClickNode', 'ClickNode']
        self.editor = editor

        self.create_content().pack_configure(fill='both', expand=False)

    def create_content(self) -> CTkFrame:
        self.frame = CTkFrame(self)
        self.frame.grid_configure(row=0, column=0)
        self.type_node_menu = CTkOptionMenu(self.frame, values=self.node_names, width=200)
        self.type_node_menu.grid_configure(row=0, column=0, padx=10, pady=10)
        self.type_node_menu.set(get_settings().get_ui_text(Texts.macros_editor_type_node_menu_placeholder))

        add_node_button = CTkButton(self.frame, text=get_settings().get_ui_text(Texts.macros_editor_add_node_button), command=self.add_node)
        add_node_button.grid_configure(row=0, column=1, padx=10, pady=10)

        self.clear_all_button = CTkButton(self.frame, text='Очистити', command=self.clear_all, fg_color='red')

        return self.frame
    
    def clear_all(self):
        self.editor.clear_all()
        self.clear_all_button.grid_forget()
    
    def add_node(self):
        type_node = self.type_node_menu.get()
        if type_node in self.node_names:
            if self.editor.no_info:
                self.editor.no_info.pack_forget()
            self.clear_all_button.grid_configure(row=0, column=2, padx=(0, 10), pady=10)
            
            new_node = NodeFactory.create_node(type_node)

            if self.editor.macros:
                self.editor.macros.add_node(new_node)
                self.pack_node(self.editor)
            else:
                self.editor.script.add_node(new_node)
                self.pack_node(self.editor)


    def pack_node(self, editor: MacrosEditor):
        editor.update_node_views()



    
class NodeViewManipulator(CTkFrame):
    def __init__(self, master: Any, up_callback: Callable, down_callback: Callable, remove_callback: Callable, **kwargs):
        super().__init__(master, **kwargs)
        self.master
        self.up_callback = up_callback
        self.down_callback = down_callback
        self.remove_callback = remove_callback

        self.create_content().pack_configure(fill='both', expand=True)
    
    def create_content(self) -> CTkFrame:
        self.frame = CTkFrame(self, fg_color='transparent', bg_color='transparent',)

        trash_img = load_img(get_settings().root_path.joinpath('src/icons/delete-trash.png'), resize=(40, 40))
        ctk_trash_img = CTkImage(trash_img)

        lift_up_node_button = CTkButton(self.frame, height=30, width=50, text='<', fg_color='transparent', command=self.up_callback)
        lift_down_node_button = CTkButton(self.frame, height=30, width=50, text='>', fg_color='transparent', command=self.down_callback)
        remove_button = CTkButton(self.frame, width=50, height=50, fg_color='red', image=ctk_trash_img, text='', command=self.remove_callback)    
        
        lift_up_node_button.pack_configure()
        remove_button.pack_configure(expand=True)
        lift_down_node_button.pack_configure()

        self.frame.grid_configure(row=0, column=2, sticky='nes', padx=(30, 0))

        return self.frame


class NodeView(CTkFrame):
    def __init__(self, master: Any, editor: MacrosEditor, node: BaseScriptNode, path_to_img: str = None, height: int = 200, color: str = '#2b2b2b', **kwargs):
        super().__init__(master, **kwargs)
        self.height = height
        self.color = color
        self.path_to_img = path_to_img
        self.editor = editor
        self.node = node
        self.node_id = node.uuid
        self.alert: CTkToplevel = None
        self.create_content().pack_configure(fill='both', expand=True)

    
    def fill_from_node(self, node: BaseScriptNode):
        node_name: NodeName = node.name
        match node_name:
            case 'ClickNode':
                return ClickNodeInfoView(self.frame, node)
            case 'TemplateClickNode':
                return TemplateClickNodeInfoView(self.frame, node)

    def create_content(self) -> CTkFrame:
        self.frame = CTkFrame(self, height=self.height, fg_color='transparent', bg_color='transparent', corner_radius=50)

        self.frame.grid_columnconfigure([1], weight=1)

        if self.path_to_img:
            img = self.load_img(self.path_to_img, (150, 150))
            img_view = CTkImage(img, size = img.size)

            image_label = CTkLabel(self.frame, image=img_view, text="", height=self.height, width=self.height)
            
            image_label.grid_configure(row=0, column=0, padx=5, pady=5, sticky='nws')
        else:
            fill_label = CTkLabel(self.frame, text="Empty data", height=self.height, width=self.height)
            
            fill_label.grid_configure(row=0, column=0, padx=5, pady=5, sticky='nws')
        
        # INFO FRAME
        """ info_frame = CTkFrame(self.frame, height=self.height, fg_color='transparent') """
        
        data = self.fill_from_node(self.node)

        

        """ name_entry = CTkEntry(info_frame, width=200,  placeholder_text=get_settings().get_ui_text(Texts.macros_editor_name_entry_placeholder))
        name_entry.pack_configure(anchor='w', fill='x', expand=False)

        desc_entry_label = CTkLabel(info_frame, text=get_settings().get_ui_text(Texts.macros_editor_desc_entry_label))
        desc_entry = CTkTextbox(info_frame,  height=80, width=400, border_width=2, border_color='black')
        
        desc_entry_label.pack_configure(anchor='nw', expand=False, pady=(20, 0))
        desc_entry.pack_configure(anchor='w', fill='x', expand=False) """

        #info_frame.grid_configure(row=0, column=1, sticky='nwse', pady=20)
        data.grid_configure(row=0, column=1, sticky='nwse', pady=20)
        
        # END INFO FRAME

        # MANIPULATOR FRAME
        #manipulator_frame = CTkFrame(self.frame, height=140)
        manipulator_frame = NodeViewManipulator(self.frame, up_callback=self.lift_up_callback, down_callback=self.lift_down_callback, remove_callback=self.show_remove_alert)
        manipulator_frame.grid_configure(row=0, column=2, sticky='nes', padx=(30, 0))
        """ trash_img = self.load_img(get_settings().root_path.joinpath('src/icons/delete-trash.png'), resize=(40, 40))
        ctk_trash_img = CTkImage(trash_img)

        lift_up_node_button = CTkButton(manipulator_frame, height=30, width=50, text='<', fg_color='transparent', command=self.lift_up_callback)
        lift_down_node_button = CTkButton(manipulator_frame, height=30, width=50, text='>', fg_color='transparent', command=self.lift_down_callback)
        remove_button = CTkButton(manipulator_frame, width=50, height=50, fg_color='red', image=ctk_trash_img, text='', command=self.show_remove_alert)
        

        #self.tooltip = ToolTip(info_tooltip, msg=f'{self.node_id}', follow=True)
        
        
        lift_up_node_button.pack_configure()
        remove_button.pack_configure(expand=True)
        lift_down_node_button.pack_configure()

        manipulator_frame.grid_configure(row=0, column=2, sticky='nes', padx=(30, 0))
        # END MANIPULATOR FRAME """

        return self.frame

    def lift_up_callback(self):      
        (old_position, new_position) = self.editor.script.lift_up_node_order(self.node_id)
        if old_position == new_position:
            return
        self.editor.editing_node_views[old_position].pack_configure(before=self.editor.editing_node_views[new_position])
        
        old = self.editor.editing_node_views[old_position]
        self.editor.editing_node_views.insert(new_position, old)
        self.editor.editing_node_views.pop(old_position + 1)

    def lift_down_callback(self):
        (old_position, new_position) = self.editor.script.lift_down_node_order(self.node_id)
        if old_position == new_position:
            return
        self.editor.editing_node_views[old_position].pack_configure(after=self.editor.editing_node_views[new_position])
        
        old = self.editor.editing_node_views[old_position]
        self.editor.editing_node_views.insert(new_position + 1, old)
        self.editor.editing_node_views.pop(old_position)

    def remove_alert(self):
        self.alert.destroy()
        self.alert = None
    
    def show_remove_alert(self):
        if self.alert is None or not self.alert.winfo_exists():
            self.alert = Alert(callback_confirm=self.remove_node, callback_discard=self.remove_alert, confirm_btn_text='Так', discard_btn_text='Ні', msg='Чи хочете ви видалити вузол?')
        else:
            self.alert.focus()
    
    def remove_node(self):
        self.editor.remove_node(self.node_id)
        self.alert.destroy()
        self.alert = None
        self.destroy()
        
    def load_img(self, path: str, resize: Tuple[int, int] = None):
        img = ImageFactory.open(path)
        if resize:
            return self.resize_img(img, resize)
        return img
    
    def resize_img(self, img: Image, size: Tuple[int, int]):
        (current_width, current_height) = img.size
        (max_width, max_height) = size

        if current_width > max_width or current_height > max_height:
            if current_width / max_width > current_height / max_height:
                new_width = max_width
                new_height = int(current_height * (new_width / current_width))
            else:
                new_height = max_height
                new_width = int(current_width * (new_height / current_height))
        else:
            new_width = current_width
            new_height = current_height
            
        resized_img = img.resize((new_width, new_height))

        return resized_img


class ImagePointView(CTkFrame):
    def __init__(self, master: Any, **kwargs):
        super().__init__(master, **kwargs)
        
    def create_content(self) -> CTkFrame:
        self.frame = CTkFrame(self)

        return self.frame

class ClickNodeInfoView(CTkFrame):
    def __init__(self, master: Any, node: ClickNode = None, **kwargs):
        super().__init__(master, **kwargs)
        self.node = node

        self.create_content().pack_configure(fill='both', expand=True)

    def create_content(self):
        self.frame = CTkFrame(self, fg_color='transparent', bg_color='transparent')

        row_1 = CTkFrame(self.frame)
        info = CTkLabel(row_1, text=f'Node: {self.node.name}', anchor='w')
        info.pack_configure(fill='both', expand=True)
        row_1.pack_configure(fill='x', expand=False, padx=5, pady=(10, 5))

        row_2 = CTkFrame(self.frame)
        row_2.grid_columnconfigure([1,3], weight=1)
        x_label = CTkLabel(row_2, text='X:', anchor='w')
        x_label.grid_configure(row=0, column=0, sticky='w', padx=(0, 10))
        self.x_input = CTkEntry(row_2)
        self.x_input.grid_configure(row=0, column=1, sticky='we', padx=(0, 10))
        y_label = CTkLabel(row_2, text='Y:', anchor='w')
        y_label.grid_configure(row=0, column=2, sticky='w', padx=(0, 10))
        self.y_input = CTkEntry(row_2)
        self.y_input.grid_configure(row=0, column=3, sticky='we', padx=(0, 10))
        row_2.pack_configure(fill='x', expand=False, padx=5, pady=5)

        row_3 = CTkFrame(self.frame)
        button_type_label = CTkLabel(row_3, text='Клавіша миші:')
        button_type_label.grid_configure(row=0, column=0, sticky='w', padx=(0, 10))
        self.button_type = CTkComboBox(row_3, values=['left', 'right'])
        self.button_type.grid_configure(row=0, column=1, sticky='w')
        count_of_click_label = CTkLabel(row_3, text='Кліків:')
        count_of_click_label.grid_configure(row=0, column=2, sticky='w', padx=(10, 10))
        self.count_of_click = CTkEntry(row_3, width=50)
        self.count_of_click.grid_configure(row=0, column=3, sticky='w', padx=(0, 10))
        row_3.pack_configure(fill='x', expand=False, padx=5, pady=5)

        row_4 = CTkFrame(self.frame)
        use_move_label = CTkLabel(row_4, text='Показувати переміщення:')
        use_move_label.grid_configure(row=0, column=0, sticky='w')
        self.use_move = CTkCheckBox(row_4, text='')
        self.use_move.grid_configure(row=0, column=1, padx=(10, 0))
        row_4.pack_configure(fill='x', expand=True, padx=5, pady=(5, 10))

        if self.node:
            self.fill_from_node(self.node)

        return self.frame
    
    def fill_from_node(self, node: ClickNode):
        self.x_input.insert(0, str(node.x))
        self.y_input.insert(0, str(node.y))
        self.button_type.set(node.button)
        self.count_of_click.insert(0, str(node.count))
        self.use_move.toggle(int(node.move))


class TemplateClickNodeInfoView(CTkFrame):
    def __init__(self, master: Any, node: ClickNode = None, **kwargs):
        super().__init__(master, **kwargs)
        self.node = node

        self.create_content().pack_configure(fill='both', expand=True)

    def create_content(self):
        self.frame = CTkFrame(self, fg_color='transparent', bg_color='transparent')

        row_1 = CTkFrame(self.frame)
        info = CTkLabel(row_1, text=f'Node: {self.node.name}', anchor='w')
        info.pack_configure(fill='both', expand=True)
        row_1.pack_configure(fill='x', expand=False, padx=5, pady=(10, 5))


        row_2 = CTkFrame(self.frame)
        button_type_label = CTkLabel(row_2, text='Клавіша миші:')
        button_type_label.grid_configure(row=0, column=0, sticky='w', padx=(0, 10))
        self.button_type = CTkComboBox(row_2, values=['left', 'right'])
        self.button_type.grid_configure(row=0, column=1, sticky='w')
        count_of_click_label = CTkLabel(row_2, text='Кліків:')
        count_of_click_label.grid_configure(row=0, column=2, sticky='w', padx=(10, 10))
        self.count_of_click = CTkEntry(row_2, width=50)
        self.count_of_click.grid_configure(row=0, column=3, sticky='w', padx=(0, 10))
        row_2.pack_configure(fill='x', expand=False, padx=5, pady=5)

        row_3 = CTkFrame(self.frame)
        use_move_label = CTkLabel(row_3, text='Показувати переміщення:')
        use_move_label.grid_configure(row=0, column=0, sticky='w')
        self.use_move = CTkCheckBox(row_3, text='')
        self.use_move.grid_configure(row=0, column=1, padx=(10, 0))
        row_3.pack_configure(fill='x', expand=False, padx=5, pady=(5, 10))

        if self.node:
            self.fill_from_node(self.node)

        return self.frame
    
    def fill_from_node(self, node: ClickNode):
        self.button_type.set(node.button)
        self.count_of_click.insert(0, str(node.count))
        self.use_move.toggle(int(node.move))