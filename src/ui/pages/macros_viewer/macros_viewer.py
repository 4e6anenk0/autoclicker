from typing import Any
from customtkinter import CTkFrame

from settings.settings import Settings
from src.ui.pages.page import Page


class MacrosViewer(Page):
    def __init__(self, master: Any, settings: Settings, **kwargs):
        super().__init__(master, settings, **kwargs)

    
    def create_content(self) -> CTkFrame:
        self.frame = CTkFrame()

        

        return self.frame