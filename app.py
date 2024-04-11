from typing import Tuple
import customtkinter as ct
from async_tkinter_loop.mixins import AsyncCTk

from src.clicker.models.macros_manager import MacrosManager
from src.settings.settings import Settings, Texts, get_settings
from src.ui.pages.mainframe import MainFrame
from src.ui.widgets.sidebar_button import SidebarButton
from src.ui.pages.page import PageManager, Pages



class App(ct.CTk, AsyncCTk):
    def __init__(self, settings: Settings):
        super().__init__()

        self.__settings = settings
        self.geometry(f"{1100}x{580}")
        self.title("Autoclicker")

        self.minsize(850, 300)

        self.macros_manager = MacrosManager(workdir=get_settings().macroses_path, path_to_metadata=get_settings().macroses_path.joinpath('metadata.json'))
        
        self.macros_manager.load_global_metadata()

        self.page_manager = PageManager()

        self.mainframe = MainFrame(self, settings=settings, page_manager=self.page_manager, macros_manager=self.macros_manager)
        self.mainframe.pack_configure(fill="both", expand=True)
        
    @property
    def settings(self) -> Settings:
        return self.__settings

