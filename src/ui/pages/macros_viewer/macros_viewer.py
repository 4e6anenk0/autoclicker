from typing import Any, Callable, Tuple
from customtkinter import CTkFrame, CTkButton, CTkScrollableFrame, CTkLabel

from src.clicker.models.macros import Macros
from src.clicker.models.macros_manager import MacrosManager
from src.settings.settings import Settings, get_settings
from src.ui.pages.page import Page, PageManager, Pages, get_page_manager
from src.ui.pages.macros_editor.macros_editor import MacrosEditor


class MacrosViewer(Page):
    def __init__(self, master: Any, settings: Settings, macros_manager: MacrosManager, **kwargs):
        super().__init__(master, settings, **kwargs)    
        self.page_manager = PageManager()
        self.macros_manager = macros_manager
        self.macros_views: list[MacrosView] = []
        self.create_content().pack_configure(fill='both', expand=True)
        self.batcher = self.macros_manager.load_macroses(2)

    def get_macroses(self):
        #macros_batcher = self.macros_manager.load_macroses(batch_size)
        
        macroses = next(self.batcher)
        print(f'Bather: {macroses}')
        if macroses:
            for macros in macroses:
                if macros:
                    view = MacrosView(self.scrollable_content, macros=macros)
                    view.pack_configure(fill='x', expand=False, pady=10)
                    self.macros_views.append(view)

  
    def create_content(self) -> CTkFrame:
        self.frame = CTkFrame(self)

        header = HeaderPanel(self.frame, manager=self.macros_manager, get_macroses_callback=lambda: self.get_macroses())
        header.pack_configure(fill='both', expand=False)

        self.scrollable_content = CTkScrollableFrame(self.frame)
        self.scrollable_content.pack(fill='both', expand=True)

        self.no_nodes_info = CTkLabel(self.scrollable_content, text='Немає жодних макросів...', anchor='n')

        # правильні прив'язки для роботи як в linux так і в windows
        # У Windows коліщатко миші прив’язується за допомогою <MouseWheel> методу, 
        # але для машини Linux прив’язка коліщатка миші призначена <Button-4>для прокручування вгору та <Button-5>
        self.scrollable_content.bind_all("<Button-4>", lambda e: self.scrollable_content._parent_canvas.yview("scroll", -1, "units"))
        self.scrollable_content.bind_all("<Button-5>", lambda e: self.scrollable_content._parent_canvas.yview("scroll", 1, "units"))


        #self.get_macroses()

        """ try:
            self.get_macroses()
        except Exception as e:
            print(f"Error: {e}")
            self.no_nodes_info.pack_configure(fill='x', expand=False, pady=30) """

        return self.frame
    
class MacrosView(CTkFrame):
    def __init__(self, master: Any, macros: Macros, **kwargs):
        super().__init__(master, **kwargs)
        self.macros = macros
        self.is_checked = False
        self.create_content().pack_configure(fill='both', expand=False)

    def create_content(self) -> CTkFrame:
        self.frame = CTkFrame(self, border_width=2, border_color='grey')
        label = CTkLabel(self.frame, text=self.macros.name)
        label.pack_configure(fill='x', expand=False, pady=20, padx=10)

        label.bind("<Button-1>", self.on_click)
        
        
        return self.frame

    def on_click(self, event):
        if not self.is_checked:
            self.frame.configure(border_color='#1f6aa5')
            self.is_checked = True
        else:
            self.frame.configure(border_color='grey')
            self.is_checked = False

    

class HeaderPanel(CTkFrame):
    def __init__(self, master: MacrosViewer, manager: MacrosManager, get_macroses_callback: Callable, **kwargs):
        super().__init__(master, **kwargs)
        self.manager = manager
        self.page_manager = PageManager()

        self.get_macroses_callback = get_macroses_callback

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

        select_macroses_button = CTkButton(right_frame, text='Вибрати', command= self.get_macroses_callback)
        select_macroses_button.pack_configure(side='right', pady=10, padx=(10, 5))

        right_frame.grid_configure(row=0, column=1, sticky='nes')

        return self.frame

    def add_macros(self):
        frame = self.page_manager.get_binding_from_page(Pages.macros_editor)
        macros = Macros(self.manager.workdir)
        page = MacrosEditor(frame, self.manager, get_settings(), macros)
        
        self.page_manager.create_and_go(Pages.macros_editor, page)
        
        
    
    def show_remove_btn(self):
        self.remove_button.pack_configure(side='right', pady=10, padx=(5, 5))

    def hide_remove_btn(self):
        self.remove_button.pack_forget()
    
    