from typing import Any
from customtkinter import CTkFrame, CTkLabel

from src.settings.settings import Settings, Texts
from src.ui.pages.page import Page


class HomePage(Page):
    def __init__(self, master: Any, settings: Settings, **kwargs):
        super().__init__(master, settings, **kwargs)

        self.create_content().pack_configure(fill='both', expand=True)

    def create_content(self) -> CTkFrame:
        self.frame = CTkFrame(self, fg_color='#F57D1F')
        text = self.settings.get_ui_text(Texts.home_page_label)
        title = CTkLabel(self.frame, text=text)
        title.pack_configure(fill="both", expand="True")
        
        return self.frame