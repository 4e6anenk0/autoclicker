from typing import Any, Dict, Protocol, Tuple, Callable, Union

from src.settings.settings import Settings, Texts
from src.ui.pages.page import Page, PageManager, ScrollablePage
from src.ui.pages.settings import SettingsPage
from src.ui.pages.home import HomePage
from customtkinter import CTkFrame

from src.ui.widgets.screenshot_action import ScreenshotAction
from src.ui.widgets.sidebar_button import SidebarButton
from src.ui.pages.macros_editor.macros_editor import MacrosEditor
from src.ui.pages.macros_viewer.macros_viewer import MacrosViewer
#from src.ui.pages._macros_editor import MacrosEditor

class AppProtocol(Protocol):
    def update():
        pass

class MainFrame(Page):
    
    def __init__(self, master: AppProtocol, settings: Settings, **kwargs):
        super().__init__(master, settings, **kwargs)

        self.master = master

        self.page_manager = PageManager()

        """ self.__pages: Dict[str, Union[Page, ScrollablePage]] = {}
        self.__default_page: str = None
        self.__current_page: str = None """

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.page_frame = CTkFrame(self)

        self.create_sidebar().grid_configure(row=0, column=0, sticky='wns')
        self.page_frame.grid_configure(row=0, column=1, sticky='wsne')
        
        self.init_pages()

    def register_page_builders(self):
        self.page_manager.register_builder('MacrosEditor', lambda: MacrosEditor(self.page_frame, settings=self.settings))
        self.page_manager.register_builder('MacrosViewer', lambda: MacrosViewer(self.page_frame, settings=self.settings))
        """ match page_name:
            case 'SettingsPage':
                return SettingsPage(self, settings=self.settings)
            case 'HomePage':
                return HomePage(self, settings=self.settings)
            case 'MacrosEditor':
                return MacrosEditor(self, settings=self.settings)
            case 'MacrosViewer':
                return MacrosViewer(self, settings=self.settings) """

    def init_pages(self):
        
        self.page_manager.init_pages(
            {
                'SettingsPage' : SettingsPage(self.page_frame, settings=self.settings),
                'HomePage' : HomePage(self.page_frame, settings=self.settings)
            }
        )
        self.register_page_builders()
        self.page_manager.set_default_page('SettingsPage')
        self.page_manager.show_default_page()

        
        """ self.add_page(SettingsPage(self, settings=self.settings))
        self.add_page(HomePage(self, settings=self.settings)) """
        #self.add_page(MacrosEditor(self, settings=self.settings))
        #self.set_default_page('SettingsPage')
        #self.show_default_page()

    def create_sidebar(self) -> CTkFrame:
        self.sidebar = Sidebar(self, settings=self.settings, menu_btn_callback=self.on_click_menu_btn, new_macros_callback=self.show_macros_editor)
        return self.sidebar
    
    def show_screenshot_action(self):
        self.action = ScreenshotAction(self.master)
        self.action.bind('<Escape>', lambda event: self.action.destroy())
        self.action.mainloop()

    def show_macros_editor(self):
        self.page_manager.show_page('MacrosEditor')
        #self.show_page('MacrosEditor')

    def on_click_menu_btn(self, page_name: str):
        self.page_manager.show_page(page_name)
        
    
    """ def show_default_page(self):
        print(self.__default_page)
        self.__pages[self.__default_page].grid_configure(row=0, column=1, sticky='wsne')
        self.__current_page = self.__default_page
    
    def show_page(self, page_name: str):
        if page_name not in self.__pages.keys():
            self.__pages[page_name] = self.page_builder(page_name)

        if self.__current_page == None:
            self.__pages[page_name].grid_configure(row=0, column=1, sticky='wsne')
            self.__current_page = page_name
        elif self.__current_page != page_name:
            self.__pages[self.__current_page].grid_remove()
            self.__pages[page_name].grid_configure(row=0, column=1, sticky='wsne')
            self.__current_page = page_name
        else:
            return
        

    def hide_page(self, page_name: str):
        if self.__current_page == page_name:
            self.__pages[page_name].grid_remove()

    def remove_page(self, page_name: str):
        if self.__current_page == page_name:
            self.__pages[page_name].destroy()

    def add_page(self, page: Union[Page, ScrollablePage]) -> Union[Page, ScrollablePage]:
        self.__pages[page.__class__.__name__] = page

    def set_default_page(self, page_name: str):
        self.__default_page = page_name

    def on_click_menu_btn(self, page_name: str):
        self.show_page(page_name) """
        

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

        self.create_content().pack_configure(fill='both', expand=True)
    
    def create_content(self) -> CTkFrame:
        self.frame = CTkFrame(self)

        self.sidebar_btn_1 = SidebarButton(self.frame, settings=self.settings, text=Texts.new_macros_btn, command=self.new_macros_callback)
        self.sidebar_btn_1.grid_configure(row=0, column=0, padx=20, pady=10)

        self.sidebar_btn_2 = SidebarButton(self.frame, settings=self.settings, text=Texts.home_btn, command=lambda: self.menu_btn_callback('HomePage'))
        self.sidebar_btn_2.grid_configure(row=1, column=0, padx=20, pady=10)

        self.sidebar_btn_3 = SidebarButton(self.frame, settings=self.settings, text=Texts.macroses_viewer_btn, command=lambda: self.menu_btn_callback('MacrosViewer'))
        self.sidebar_btn_3.grid_configure(row=2, column=0, padx=20, pady=10)

        self.sidebar_btn_4 = SidebarButton(self.frame, settings=self.settings, text=Texts.settings_btn, command=lambda: self.menu_btn_callback('SettingsPage'))
        self.sidebar_btn_4.grid_configure(row=3, column=0, padx=20, pady=10)

        return self.frame

        
        