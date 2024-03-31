from typing import Any, Callable, Tuple
from customtkinter import CTkFrame, CTkScrollableFrame

from src.settings.settings import Settings


class Page(CTkFrame):
    def __init__(self, master: Any, settings: Settings, **kwargs):
        super().__init__(master, **kwargs)
        self.__settings = settings
        self.frame: CTkFrame = None
        self.__master = master

    @property
    def settings(self):
        return self.__settings
    
    def update_all(self):
        self.__master.update_all()
    

class ScrollablePage(CTkScrollableFrame):
    def __init__(self, master: Any, settings: Settings, **kwargs):
        super().__init__(master, **kwargs)
        self.__settings = settings
        self.frame: CTkScrollableFrame = None
        self.__master = master

    @property
    def settings(self):
        return self.__settings
    
    def update_all(self):
        self.__master.update_all()