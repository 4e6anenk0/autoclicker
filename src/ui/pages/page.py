from typing import Any, Callable, Dict, Tuple, Union
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
    
    def show_page(self):
        pass

    def hide_page(self):
        pass
    
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


class PageManager:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        self.__pages: Dict[str, Union[Page, ScrollablePage]] = {}
        self.__page_builders: Dict[str, Callable] = {}
        self.__default_page: str = None
        self.__current_page: str = None

    def register_builder(self, name: str, builder: Callable):
        self.__page_builders[name] = builder

    def page_builder(self, name: str):
        if name in self.__page_builders.keys():
            page = self.__page_builders[name]()
            self.__pages[name] = page
            return page
        else:
            raise ValueError(f'Not founded builder for the name: {name}')

    def add_page(self, name: str, page: Page):
        self.__pages[name] = page

    def _show_frame(self, name: str):
        if name not in self.__pages.keys():
            try: 
                page = self.page_builder(name)
            except:
                raise ValueError(f'Cant show the Page for this name: {name}')
        
        if self.__current_page == None:
            
            self.__pages[name].pack_configure(fill='both', expand=True)
            self.__current_page = name
        elif self.__current_page != name:
            self.__pages[self.__current_page].pack_forget()
            page = self.__pages.get(name)
            page.pack_configure(fill='both', expand=True)
            self.__current_page = name
        else:
            return
            
    def show_page(self, name: str):
        self._show_frame(name)

    def hide_page(self, name: str):
        self.__pages.get(name).pack_forget()

    def remove_page(self, name: str):
        self.__pages.get(name).destroy()

    def show_default_page(self):
        page = self.__pages.get(self.__default_page)
        page.pack_configure(fill='both', expand=True)
        self.__current_page = self.__default_page

    def set_default_page(self, name: str):
        self.__default_page = name

    def init_pages(self, pages: Dict[str, Union[Page, ScrollablePage]]):
        for name, page in pages.items():
            self.add_page(name, page)
