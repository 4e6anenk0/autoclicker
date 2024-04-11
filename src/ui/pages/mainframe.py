from typing import Any, Protocol, Callable, Union
from customtkinter import CTkFrame

from src.clicker.models.macros_manager import MacrosManager
from src.settings.settings import Settings, Texts, get_settings
from src.ui.pages.page import Page, PageManager, Pages
from src.ui.pages.settings import SettingsPage
from src.ui.pages.home import HomePage
from src.ui.widgets.screenshot_action import ScreenshotAction
from src.ui.widgets.sidebar_button import SidebarButton
from src.ui.pages.macros_editor.macros_editor import MacrosEditor
from src.ui.pages.macros_viewer.macros_viewer import MacrosViewer


class AppProtocol(Protocol):
    def update():
        pass

class MainFrame(Page):
    
    def __init__(self, master: AppProtocol, settings: Settings, **kwargs):
        super().__init__(master, settings, **kwargs)

        self.master = master

        self.macros_manager = MacrosManager(workdir=get_settings().macroses_path, path_to_metadata=get_settings().macroses_path.joinpath('metadata.json'))
        
        self.macros_manager.load_global_metadata()

        self.page_manager = PageManager()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.page_frame = CTkFrame(self)

        self.create_sidebar().grid_configure(row=0, column=0, sticky='wns')
        self.page_frame.grid_configure(row=0, column=1, sticky='wsne')
        
        self.init_pages()

    def register_page_builders(self):
        self.page_manager.register_pages(
            {
                Pages.macros_editor : lambda: MacrosEditor(self.page_frame, settings=self.settings, macros_manager=self.macros_manager),
                Pages.macros_viewer : lambda: MacrosViewer(self.page_frame, settings=self.settings, macros_manager=self.macros_manager),
                #Pages.home          : lambda: HomePage(self.page_frame, settings=self.settings),
                Pages.settings      : lambda: SettingsPage(self.page_frame, settings=self.settings)
            }
        )

    def init_pages(self):
        self.register_page_builders()
        self.page_manager.init_pages([Pages.settings, Pages.macros_editor])
        self.page_manager.set_default_page(Pages.settings)
        self.page_manager.show_default_page()

    def create_sidebar(self) -> CTkFrame:
        self.sidebar = Sidebar(self, settings=self.settings, menu_btn_callback=self.on_click_menu_btn, new_macros_callback=self.show_macros_editor)
        return self.sidebar
    
    def show_screenshot_action(self):
        self.action = ScreenshotAction(self.master)
        self.action.bind('<Escape>', lambda event: self.action.destroy())
        self.action.mainloop()

    def show_macros_editor(self):
        self.page_manager.show_page(Pages.macros_editor, redraw_frame=True)

    def on_click_menu_btn(self, page_name: str):
        self.page_manager.show_page(page_name, redraw_frame=True)
        

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

        # self.sidebar_btn_2 = SidebarButton(self.frame, settings=self.settings, text=Texts.home_btn, command=lambda: self.menu_btn_callback(Pages.home))
        # self.sidebar_btn_2.grid_configure(row=1, column=0, padx=20, pady=10)

        self.sidebar_btn_3 = SidebarButton(self.frame, settings=self.settings, text=Texts.macroses_viewer_btn, command=lambda: self.menu_btn_callback(Pages.macros_viewer))
        self.sidebar_btn_3.grid_configure(row=2, column=0, padx=20, pady=10)

        self.sidebar_btn_4 = SidebarButton(self.frame, settings=self.settings, text=Texts.settings_btn, command=lambda: self.menu_btn_callback(Pages.settings))
        self.sidebar_btn_4.grid_configure(row=3, column=0, padx=20, pady=10)

        return self.frame

        
        