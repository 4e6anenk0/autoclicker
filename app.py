from typing import Tuple
import customtkinter as ct
from async_tkinter_loop.mixins import AsyncCTk

from src.settings.settings import Settings, Texts
from src.ui.pages.mainframe import MainFrame
from src.ui.widgets.sidebar_button import SidebarButton


class App(ct.CTk, AsyncCTk):
    def __init__(self, settings: Settings):
        super().__init__()

        self.__settings = settings
        self.geometry(f"{1100}x{580}")
        self.title("Autoclicker")

        self.minsize(700, 300)

        self.mainframe = MainFrame(self, settings=settings)
        self.mainframe.pack_configure(fill="both", expand=True)

    def update_all(self):
        updated_frame = MainFrame(self, settings=self.__settings)
        self.mainframe.destroy()
        self.mainframe = updated_frame
        self.mainframe.pack_configure(fill="both", expand=True)

    @property
    def settings(self) -> Settings:
        return self.__settings

