from typing import Any, Callable, Union
from customtkinter import CTkButton

from src.settings.settings import Settings, Texts, get_settings


class SidebarButton(CTkButton):
    def __init__(self, master: Any, text: Texts, settings: Settings, width: int = 250, height: int = 50, command: Union[Callable[[], Any], None] = None, **kwargs):
        super().__init__(master, width = width, text = settings.get_ui_text(text), height = height, command=command, **kwargs)

        