from typing import Any
from customtkinter import CTkFrame, CTkButton, CTkScrollableFrame

from src.clicker.models.macros import Macros
from src.clicker.models.macros_manager import MacrosManager
from src.settings.settings import Settings, get_settings
from src.ui.pages.page import Page


class MacrosViewer(Page):
    def __init__(self, master: Any, settings: Settings, macros_manager: MacrosManager = None, **kwargs):
        super().__init__(master, settings, **kwargs)
        
        #self.page_manager = PageManager()
        
        self.workdir = get_settings().macroses_path
        self.macros_manager = macros_manager if macros_manager else MacrosManager(workdir=self.workdir, 
                                                                                  path_to_metadata=self.workdir.joinpath('metadata.json'))
        self.macros_manager.load_global_metadata()

        self.create_content().pack_configure(fill='both', expand=True)

        #self.get_macroses(batch_size=3)


    def get_macroses(self, batch_size: int):
        macros_batcher = self.macros_manager.load_macroses(batch_size)
        print(next(macros_batcher))



    
    def create_content(self) -> CTkFrame:
        self.frame = CTkFrame(self)

        header = HeaderPanel(self.frame, manager=self.macros_manager)
        header.pack_configure(fill='both', expand=False)

        self.scrollable_content = CTkScrollableFrame(self.frame)
        self.scrollable_content.pack(fill='both', expand=True)

        # правильні прив'язки для роботи як в linux так і в windows
        # У Windows коліщатко миші прив’язується за допомогою <MouseWheel> методу, 
        # але для машини Linux прив’язка коліщатка миші призначена <Button-4>для прокручування вгору та <Button-5>
        self.scrollable_content.bind_all("<Button-4>", lambda e: self.scrollable_content._parent_canvas.yview("scroll", -1, "units"))
        self.scrollable_content.bind_all("<Button-5>", lambda e: self.scrollable_content._parent_canvas.yview("scroll", 1, "units"))

        return self.frame
    

class HeaderPanel(CTkFrame):
    def __init__(self, master: MacrosViewer, manager: MacrosManager, **kwargs):
        super().__init__(master, **kwargs)
        self.manager = manager
        


        self.create_content().pack_configure(fill='both', expand=False)

    def create_content(self) -> CTkFrame:
        self.frame = CTkFrame(self)
        self.frame.grid_configure(row=0, column=0)
        
        self.frame.grid_columnconfigure([1], weight=1)

        add_macros_button = CTkButton(self.frame, text='Додати макрос', command=self.add_macros)
        add_macros_button.grid_configure(row=0, column=0, padx=10, pady=10, sticky='nws')

        right_frame = CTkFrame(self.frame, fg_color='transparent', bg_color='transparent')

        self.remove_button = CTkButton(right_frame, text='Видалити', fg_color='red')
        self.remove_button.pack_configure(side='right', pady=10, padx=(5, 10))

        remove_all_button = CTkButton(right_frame, text='Видалити все', fg_color='red')
        remove_all_button.pack_configure(side='right', pady=10, padx=(5, 5))

        select_macroses_button = CTkButton(right_frame, text='Вибрати')
        select_macroses_button.pack_configure(side='right', pady=10, padx=(10, 5))

        right_frame.grid_configure(row=0, column=1, sticky='nes')

        return self.frame
    
    def add_macros(self):
        """ macros = Macros(self.manager.workdir)
        self.manager.add_macros(macros)
        self.page_manager.show_page('MacrosEditor', macros=macros) """
        
    
    def show_remove_btn(self):
        self.remove_button.pack_configure(side='right', pady=10, padx=(5, 5))

    def hide_remove_btn(self):
        self.remove_button.pack_forget()
    
    