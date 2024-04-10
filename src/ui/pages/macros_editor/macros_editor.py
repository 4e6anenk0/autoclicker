from customtkinter import CTkFrame, CTkScrollableFrame, CTkFont, CTkEntry, CTkButton, CTkLabel, CTkOptionMenu
from typing import Any

from src.clicker.models.macros_manager import MacrosManager
from src.clicker.models.nodes.node_factory import NodeFactory, NodeName
from src.clicker.models.nodes.base_node import BaseScriptNode
from src.clicker.models.script import Script
from src.clicker.models.macros import Macros
from src.settings.settings import Settings, Texts, get_settings
from src.ui.pages.page import Page
from src.ui.pages.macros_editor.node_view_manager import NodeViewManager
from src.ui.pages.macros_editor.node_view_builder import NodeViewBuilder


class MacrosEditor(Page):
    def __init__(self, master: Page, macros_manager: MacrosManager, settings: Settings, macros: Macros = None, **kwargs):
        super().__init__(master, settings, **kwargs)
        self.macros = macros
        self.script = Script() if not macros else macros.script
        self.macros_manager = macros_manager
        self.node_manager = NodeViewManager(self.script)
        self.node_view_builder = NodeViewBuilder(self.node_manager)
        self.no_nodes_info = None
        
        self.create_content().pack_configure(fill='both', expand=True)
        
        self.fill_data_from_macros_if_exist()

    

    def create_content(self) -> CTkFrame:
        self.frame = CTkFrame(self)
        
        self.header = CTkFrame(self)
        self.header.pack_configure(fill='both', expand=False)
        
        self.scrollable_content = CTkScrollableFrame(self.frame)
        self.scrollable_content.pack(fill='both', expand=True)

        self.no_nodes_info = CTkLabel(self.scrollable_content, text=get_settings().get_ui_text(Texts.macros_editor_no_info_label), anchor='n')

        # правильні прив'язки для роботи як в linux так і в windows
        # У Windows коліщатко миші прив’язується за допомогою <MouseWheel> методу, 
        # але для машини Linux прив’язка коліщатка миші призначена <Button-4> для прокручування вгору та <Button-5>
        self.scrollable_content.bind_all("<Button-4>", lambda e: self.scrollable_content._parent_canvas.yview("scroll", -1, "units"))
        self.scrollable_content.bind_all("<Button-5>", lambda e: self.scrollable_content._parent_canvas.yview("scroll", 1, "units"))
        
        title_frame = CTkFrame(self.header, fg_color='transparent')
        title_frame.grid_columnconfigure(1, weight=1)
        
        self.title = CTkEntry(title_frame, font=CTkFont(size=20, weight='bold'), placeholder_text=get_settings().get_ui_text(Texts.macros_editor_title_placeholder), width=400)
        self.title.grid_configure(row=0, column=0, sticky='w')

        """ metadata_info = CTkButton(title_frame, width=100, height=42, text='info', command=self.open_metadata_info)
        metadata_info.grid_configure(row=0, column=1, sticky='w', padx=10) """

        save_macros_button = CTkButton(title_frame, text=get_settings().get_ui_text(Texts.macros_editor_save_macros_button), height=42, fg_color='green', command=self.save)
        save_macros_button.grid_configure(row=0, column=2, sticky='e')

        title_frame.pack_configure(padx=10, pady=10, fill='x', expand=True)

        header_panel = HeaderPanel(self.header, editor=self)
        header_panel.pack_configure(anchor='w')
        
        if self.macros: # Заповнення scrollable_content або існуючими вузлами в макросі, або повідомленням їх відсутності
            for node in self.macros.get_nodes():
                node_view = self.node_view_builder.get_view(self.scrollable_content, node)

                self.editing_node_views.append(node_view) ## можливий баг
                node_view.pack_configure(padx=(0, 10), pady=10) 
        else:
            #self.no_nodes_info = 
            self.no_nodes_info.pack_configure(pady=30)

        return self.frame
    
    
    
    """ def open_metadata_info(self):
        self.metadata_info = MetadataInfo(macros=self.macros)
        self.metadata_info.focus() """

    def fill_data_from_macros_if_exist(self):
        print('fill_data_from_macros_if_exist')
        print(self.macros)
        if self.macros:
            print(self.macros.name)
            #self.title.delete(0)
            self.title.insert(0, string=self.macros.name)
    
    def save(self):
        if self.check_data_to_save(): 
            if not self.macros:
                self.macros = Macros(get_settings().macroses_path, name=self.title.get())
            
            self.node_manager.set_path_to_data(str(self.macros.get_macros_path().joinpath('data/')))
            
            self.node_manager.synchronize_data_from_view()
            self.node_manager.editing_nodes_to_script()
            self.macros.add_script(self.script)
            self.update_macros_data()
            self.macros_manager.add_macros(self.macros)
            self.macros_manager.save_all_macroses()
            
            self.node_manager.save_images()
            #self.node_manager.save_images(str(self.macros.macros_path.joinpath('data/')))
        
        self.clear_all()

    def update_macros_data(self):
        self.macros.set_name(self.title.get())
        

    def check_data_to_save(self) -> bool:
        if not self.title.get():
            self.title.configure(border_width = 2, border_color = 'red')
            return False
        else: 
            self.title.configure(border_width = 2, border_color = '#565b5e')
            return True

    def clear_all(self):
        self.title.delete(0, len(self.title.get()))
        self.node_manager.clear_all()
        self.macros = None
        self.script = Script()
        self.node_manager.script = self.script
        self.show_no_data_info()

    def show_no_data_info(self):
        self.no_nodes_info.pack_configure(pady=30)

    def create_node_view(self, node: BaseScriptNode):
        return self.node_view_builder.get_view(self.scrollable_content, node)

    def update_node_views(self):
        for node in self.script.get_nodes():
            if node.uuid not in self.node_manager.editing_nodes:
                self.node_manager.editing_nodes[node.uuid] = node

                node_view = self.create_node_view(node)
                    
                self.node_manager.editing_node_views.append(node_view)
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
        self.hide_clear_all_button()

    def hide_clear_all_button(self):
        self.clear_all_button.grid_forget()
    
    def show_clear_all_button(self):
        self.clear_all_button.grid_configure(row=0, column=2, padx=(0, 10), pady=10)
    
    def add_node(self):
        type_node = self.type_node_menu.get()
        if type_node in self.node_names:
            if self.editor.no_nodes_info:
                self.editor.no_nodes_info.pack_forget()
            self.show_clear_all_button() 
            
            new_node = NodeFactory.create_node(type_node)

            self.editor.node_manager.add_node(new_node)
            self.pack_node()


    def pack_node(self):
        self.editor.update_node_views()