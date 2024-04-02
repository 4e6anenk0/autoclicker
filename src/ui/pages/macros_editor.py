from copy import copy
from typing import Any, Callable, Dict, Tuple
import customtkinter
from customtkinter import CTkFrame, CTkLabel, CTkScrollableFrame, CTkOptionMenu, CTkFont, CTkImage, CTkEntry, CTkTextbox, CTkButton, CTkToplevel
from PIL.Image import Image
from PIL import Image as ImageFactory
from src.clicker.models.nodes.base_node import BaseScriptNode
from src.clicker.models.script import Script
from src.clicker.models.macros import Macros
from src.clicker.models.nodes.node_factory import NodeFactory, NodeName
from src.settings.settings import Settings, Texts, get_settings
from src.ui.pages.page import ScrollablePage, Page


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

        save_macros_button = CTkButton(title_frame, text=get_settings().get_ui_text(Texts.macros_editor_save_macros_button), height=42, fg_color='green')
        save_macros_button.grid_configure(row=0, column=1, sticky='e')

        title_frame.pack_configure(padx=10, pady=10, fill='x', expand=True)

        header_panel = HeaderPanel(self.header, editor=self)
        header_panel.pack_configure(anchor='w')
        
        if self.macros:
            for node in self.macros.get_nodes():
                node_view = NodeView(self.scrollable_content, self, path_to_img=node.get_data)
                self.editing_node_views.append(node_view)
                node_view.pack_configure(padx=(0, 10), pady=10)
            
        else:
            self.no_info = CTkLabel(self.scrollable_content, text=get_settings().get_ui_text(Texts.macros_editor_no_info_label), anchor='n')
            self.no_info.pack_configure(pady=30)

        return self.frame
    
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

    def update_node_views(self):
        print(self.editing_node_views)
        for node in self.script.get_nodes():
            if node.uuid not in self.editing_nodes:
                self.editing_nodes[node.uuid] = node
                node_view = NodeView(self.scrollable_content, self, node_id = node.uuid, path_to_img=node.get_data())
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


class NodeView(CTkFrame):
    def __init__(self, master: Any, editor: MacrosEditor, node_id: str, path_to_img: str = None, height: int = 200, color: str = '#2b2b2b', **kwargs):
        super().__init__(master, **kwargs)
        self.height = height
        self.color = color
        self.path_to_img = path_to_img
        self.editor = editor
        self.node_id = node_id
        self.alert: CTkToplevel = None
        self.create_content().pack_configure(fill='both', expand=True)
        

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
        info_frame = CTkFrame(self.frame, height=self.height, fg_color='transparent')
        
        name_entry = CTkEntry(info_frame, width=200,  placeholder_text=get_settings().get_ui_text(Texts.macros_editor_name_entry_placeholder))
        name_entry.pack_configure(anchor='w', fill='x', expand=False)

        desc_entry_label = CTkLabel(info_frame, text=get_settings().get_ui_text(Texts.macros_editor_desc_entry_label))
        desc_entry = CTkTextbox(info_frame,  height=80, width=400, border_width=2, border_color='black')
        
        desc_entry_label.pack_configure(anchor='nw', expand=False, pady=(20, 0))
        desc_entry.pack_configure(anchor='w', fill='x', expand=False)

        info_frame.grid_configure(row=0, column=1, sticky='nwse', pady=20)
        # END INFO FRAME

        # MANIPULATOR FRAME
        manipulator_frame = CTkFrame(self.frame, height=140)

        trash_img = self.load_img(get_settings().root_path.joinpath('src/icons/delete-trash.png'), resize=(40, 40))
        ctk_trash_img = CTkImage(trash_img)

        lift_up_node_button = CTkButton(manipulator_frame, height=30, width=50, text='<', fg_color='transparent', command=self.lift_up_callback)
        lift_down_node_button = CTkButton(manipulator_frame, height=30, width=50, text='>', fg_color='transparent', command=self.lift_down_callback)
        remove_button = CTkButton(manipulator_frame, width=50, height=50, fg_color='red', image=ctk_trash_img, text='', command=self.show_remove_alert)
        
        lift_up_node_button.pack_configure()
        remove_button.pack_configure(expand=True)
        lift_down_node_button.pack_configure()

        manipulator_frame.grid_configure(row=0, column=2, sticky='nes', padx=(30, 0))
        # END MANIPULATOR FRAME

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
    

class Alert(CTkToplevel):
    def __init__(self, msg: str, confirm_btn_text: str, discard_btn_text: str, callback_confirm: Callable, callback_discard: Callable, screen_size: Tuple[int, int] = (400, 300), *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry(f"{screen_size[0]}x{screen_size[1]}")
        self.msg = msg
        self.confirm_btn_text = confirm_btn_text
        self.discard_btn_text = discard_btn_text

        self.resizable(False, False)

        self.create_content(callback_confirm, callback_discard).pack_configure(fill='both', expand=True)
    
    def create_content(self, callback_confirm, callback_discard):
        self.frame = CTkFrame(self)

        self.frame.columnconfigure([0,1], weight=1)
        
        label_frame = CTkFrame(self.frame, fg_color='transparent')

        label = CTkLabel(label_frame, text=self.msg)
        label.pack_configure(fill='x', expand=True)

        buttons_frame = CTkFrame(self.frame, fg_color='transparent')

        buttons_frame.columnconfigure([0,1], weight=1)

        confirm_button = CTkButton(buttons_frame, width=120, height=30, fg_color='green', command= lambda: callback_confirm(), text=self.confirm_btn_text)
        discard_button = CTkButton(buttons_frame, width=120, height=30, fg_color='red', command= lambda: callback_discard(), text=self.discard_btn_text)

        confirm_button.grid_configure(row=0, column=0, padx=(10, 5), pady=20)
        discard_button.grid_configure(row=0, column=1, padx=(5, 10), pady=20)

        label_frame.pack_configure(fill='both', expand=True)
        buttons_frame.pack_configure(fill='x', expand=True)

        return self.frame
    

