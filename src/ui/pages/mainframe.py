from typing import Any, Dict, Protocol, Tuple, Callable, Union

from src.settings.settings import Settings, Texts
from src.ui.pages.page import Page, ScrollablePage
from src.ui.pages.settings import SettingsPage
from src.ui.pages.home import HomePage
from customtkinter import CTkFrame

from src.ui.widgets.screenshot_action import ScreenshotAction
from src.ui.widgets.sidebar_button import SidebarButton
from src.ui.pages.macros_editor import MacrosEditor

class AppProtocol(Protocol):
    def update():
        pass

class MainFrame(Page):
    
    def __init__(self, master: AppProtocol, settings: Settings, **kwargs):
        super().__init__(master, settings, **kwargs)

        self.master = master

        self.__pages: Dict[str, Union[Page, ScrollablePage]] = {}
        self.__default_page: str = None
        self.__current_page: str = None

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.create_sidebar().grid_configure(row=0, column=0, sticky='wns')

        self.init_pages()

    def init_pages(self):
        self.add_page(SettingsPage(self, settings=self.settings))
        self.add_page(HomePage(self, settings=self.settings))
        self.add_page(MacrosEditor(self, settings=self.settings))
        
        self.set_default_page('SettingsPage')
        self.show_default_page()

    def create_sidebar(self) -> CTkFrame:
        self.sidebar = Sidebar(self, settings=self.settings, menu_btn_callback=self.on_click_menu_btn, new_macros_callback=self.show_macros_editor)
        return self.sidebar
    
    def show_screenshot_action(self):
        self.action = ScreenshotAction(self.master)
        self.action.bind('<Escape>', lambda event: self.action.destroy())
        self.action.mainloop()

    def show_macros_editor(self):
        self.show_page('MacrosEditor')
        
    
    def show_default_page(self):
        print(self.__default_page)
        self.__pages[self.__default_page].grid_configure(row=0, column=1, sticky='wsne')
        self.__current_page = self.__default_page
    
    def show_page(self, page_name: str):
        if self.__current_page == None:
            self.__pages[page_name].grid_configure(row=0, column=1, sticky='wsne')
            self.__current_page = page_name
        elif self.__current_page != page_name:
            self.__pages[self.__current_page].grid_remove()
            self.__pages[page_name].grid_configure(row=0, column=1, sticky='wsne')
            self.__current_page = page_name

    def hide_page(self, page_name: str):
        if self.__current_page == page_name:
            self.__pages[page_name].grid_remove()

    def add_page(self, page: Union[Page, ScrollablePage]) -> Union[Page, ScrollablePage]:
        self.__pages[page.__class__.__name__] = page

    def set_default_page(self, page_name: str):
        self.__default_page = page_name

    def on_click_menu_btn(self, page_name: str):
        self.show_page(page_name)
        

class Sidebar(CTkFrame):
    def __init__(self, 
                 master: MainFrame, 
                 settings: Settings, 
                 width: int = 300, 
                 menu_btn_callback: Union[Callable[[str], Any], None] = None,
                 new_macros_callback: Union[Callable[[], Any], None] = None,
                 **kwargs):
        super().__init__(master, width, **kwargs)

        self.mainframe = master
        self.settings = settings
        self.menu_btn_callback = menu_btn_callback
        self.new_macros_callback = new_macros_callback

        self.create_content()
    
    def create_content(self) -> CTkFrame:
        self.sidebar_btn_1 = SidebarButton(self, settings=self.settings, text=Texts.new_macros_btn, command=self.new_macros_callback)
        self.sidebar_btn_1.grid_configure(row=0, column=0, padx=20, pady=10)

        self.sidebar_btn_2 = SidebarButton(self, settings=self.settings, text=Texts.home_btn, command=lambda: self.menu_btn_callback('HomePage'))
        self.sidebar_btn_2.grid_configure(row=1, column=0, padx=20, pady=10)

        self.sidebar_btn_3 = SidebarButton(self, settings=self.settings, text=Texts.settings_btn, command=lambda: self.menu_btn_callback('SettingsPage'))
        self.sidebar_btn_3.grid_configure(row=2, column=0, padx=20, pady=10)

        
        