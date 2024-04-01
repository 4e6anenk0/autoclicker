from typing import Any, Tuple
import customtkinter
from customtkinter import CTkFrame, CTkLabel, CTkScrollableFrame, CTkOptionMenu, CTkFont, CTkImage, CTkEntry, CTkTextbox, CTkButton
from PIL.Image import Image
from PIL import Image as ImageFactory
from src.clicker.models.macros import Macros
from src.clicker.models.nodes.node_factory import NodeName
from src.settings.settings import Settings, Texts, get_settings
from src.ui.pages.page import ScrollablePage, Page


class MacrosEditor(Page):
    def __init__(self, master: Page, settings: Settings, macros: Macros = None, **kwargs):
        super().__init__(master, settings, **kwargs)
        self.macros = macros

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
        
        text = self.settings.get_ui_text(Texts.home_page_label)
        title = CTkLabel(self.header, text=text, font=CTkFont(size=20, weight='bold'))
        
        title.pack_configure(padx=16, pady=16, anchor='w')

        header_panel = HeaderPanel(self.header)
        header_panel.pack_configure(anchor='w')
        
        body_text = CTkLabel(self.scrollable_content, text='Test body text 1', font=CTkFont(size=20, weight='bold'))
        body_text.pack_configure(anchor='w')

        #img_path = str(get_settings().root_path.joinpath('screenshot.png'))
        
        """ for _ in range(7):
            node_view = NodeView(self.scrollable_content, path_to_img=img_path)
            node_view.pack_configure(padx=(0, 10), pady=10) """
        
        if self.macros:
            for node in self.macros.get_nodes():
                node_view = NodeView(self.scrollable_content, path_to_img=node.get_data)
                node_view.pack_configure(padx=(0, 10), pady=10)
        else:
            no_info = CTkLabel(self.scrollable_content, text='No any nodes...')
            no_info.pack_configure()
        
        
        return self.frame
    
    @classmethod
    def from_macros(cls, master: Page, settings: Settings, macros: Macros, **kwargs):
        macros_editor_page = cls(master, settings, **kwargs)
        nodes = macros.get_nodes()
        for node in nodes:
            pass
    


    
class HeaderPanel(CTkFrame):
    def __init__(self, master: Any, **kwargs):
        super().__init__(master, **kwargs)
        self.nodes: NodeName = ['TemplateClickNode', 'ClickNode']

        self.create_content().pack_configure(fill='both', expand=False)

    def create_content(self) -> CTkFrame:
        self.frame = CTkFrame(self)
        self.frame.grid_configure(row=0, column=0)
        type_node_menu = CTkOptionMenu(self.frame, values=self.nodes)
        type_node_menu.grid_configure(row=0, column=0, padx=10, pady=10)
        type_node_menu.set('Type of node:')

        return self.frame


class NodeView(CTkFrame):
    def __init__(self, master: Any, path_to_img: str, height: int = 200, color: str = '#2b2b2b', **kwargs):
        super().__init__(master, **kwargs)
        self.height = height
        self.color = color
        self.path_to_img = path_to_img
        
        
        self.create_content().pack_configure(fill='both', expand=True)
        

    def create_content(self) -> CTkFrame:
        self.frame = CTkFrame(self, height=self.height, fg_color='transparent', bg_color='transparent', corner_radius=50)

        self.frame.grid_columnconfigure([1], weight=1)
        
        img = self.load_img(self.path_to_img, (150, 150))
        img_view = CTkImage(img, size = img.size)
        
        image_label = CTkLabel(self.frame, image=img_view, text="", height=self.height, width=self.height)
        image_label.grid_configure(row=0, column=0, padx=5, pady=5, sticky='nws')
        
        info_frame = CTkFrame(self.frame, height=self.height, fg_color='transparent')
        
        name_entry = CTkEntry(info_frame, width=200,  placeholder_text='Node name...')
        name_entry.pack_configure(anchor='w', fill='x', expand=False)

        desc_entry_label = CTkLabel(info_frame, text='Description:')
        desc_entry = CTkTextbox(info_frame,  height=80, width=400, border_width=2, border_color='black')
        
        desc_entry_label.pack_configure(anchor='nw', expand=False, pady=(20, 0))
        desc_entry.pack_configure(anchor='w', fill='x', expand=False)

        info_frame.grid_configure(row=0, column=1, sticky='nwse', pady=20)

        trash_img = self.load_img(get_settings().root_path.joinpath('src/icons/delete-trash.png'), resize=(40, 40))
        ctk_trash_img = CTkImage(trash_img)
        remove_button = CTkButton(self.frame, width=80, height=140, fg_color='red', image=ctk_trash_img, text='')
        remove_button.grid_configure(row=0, column=2, sticky='nes', padx=(30, 0))

        return self.frame
    
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
    


        