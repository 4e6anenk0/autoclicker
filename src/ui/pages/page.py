from enum import Enum
from threading import Lock
from typing import Any, Callable, Dict, Tuple, Union
from customtkinter import CTkFrame, CTkScrollableFrame

from src.settings.settings import Settings

class Pages(str, Enum):
    home = 'HomePage'
    macros_editor ='MacrosEditor'
    macros_viewer = 'MacrosViewer'
    settings = 'SettingsPage'

    def __str__(self) -> str:
        return self.value


class Page(CTkFrame):
    def __init__(self, master: Any, settings: Settings, **kwargs):
        super().__init__(master, **kwargs)
        self.name = __class__.__name__
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
        self.name = __class__.__name__
        self.__settings = settings
        self.frame: CTkScrollableFrame = None
        self.__master = master

    @property
    def settings(self):
        return self.__settings
    
    def update_all(self):
        self.__master.update_all()


class Singleton(type):
    _instances = {}

    def __call__(cls, *args: Any, **kwds: Any) -> Any:
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwds)
        return cls._instances[cls]

class PageManager(metaclass=Singleton):
    
    def __init__(self):
        self.__pages: Dict[str, Union[Page, ScrollablePage]] = {}
        self.__page_builders: Dict[str, Callable] = {}
        self.__binds: Dict[str, CTkFrame] = {}
        self.__default_page: str = None
        self.__current_page: str = None
        self.__marked_for_redraw: list[str] = []

    def __str__(self) -> str:
        for name in self.__pages.keys():
            print(f"PAGE NAME: {name}")

    def register_page(self, name: str, builder: Callable):
        if name in self.__page_builders.keys():
            return
        self.__page_builders[name] = builder

    def register_pages(self, page_builders: Dict[str, Callable]):
        for name, builder in page_builders.items():
            if name in self.__page_builders.keys():
                return
            self.__page_builders[name] = builder

    def page_builder(self, name: str):
        
        if name in self.__page_builders.keys():
            try:
                page_builder = self.__page_builders.get(name)
                page = page_builder()
                self.__pages[name] = page
                return page
            except Exception as e:
                print(f"Page builder EXEPTION: {e}")
        else:
            raise ValueError(f'Not founded builder for the name: {name}')

    def add_page(self, name: str, page: Page):
        if name not in self.__pages.keys():
            self.__pages[name] = page

    def set_page(self, name: str, page: Page):
        if name in self.__pages.keys():
            self.__pages[name].destroy()
        self.__pages[name] = page
        self.show_page(name)
        #self.__pages[name].pack_configure(fill='both', expand=True)

    def set_bind(self, page_name_to_bind: str, frame):
        self.__binds[page_name_to_bind] = frame

    """ def redraw_page(self, name: str):
        self.__pages[name].pack_forget()
        self.__pages[name] = self.page_builder(name) """

    """ def _redraw(self):
        if len(self.__marked_for_redraw) == 0:
            return
        for name in self.__marked_for_redraw:
            self.__pages[name].pack_forget()
            self.__pages[name] = self.page_builder(name)
        self.__marked_for_redraw = [] """

    def _redraw_page(self, name: str):
        self.__pages[name].pack_forget()
        self.__pages[name] = self.page_builder(name)

    def _backgroud_redraw(self):
        if len(self.__marked_for_redraw) == 0:
            return
        for name in self.__marked_for_redraw:
            self._redraw_page(name)
        self.__marked_for_redraw = []

    def _on_opening_redraw(self, name: str):
        if name in self.__pages.keys():
            self._redraw_page(name)
        else:
            self.__pages[name] = self.page_builder(name)

    def _show_frame(self, name: str):
        if self.__current_page == None:
            self.__pages[name].pack_configure(fill='both', expand=True)
            self.__current_page = name
        elif self.__current_page != name:
            page = self.__pages.get(name)
            self.__pages[self.__current_page].pack_forget()
            page.pack_configure(fill='both', expand=True)
            
            self.__current_page = name
        else:
            return

    def _show_page(self, name: str, redraw_frame: bool):
        """
        Метод відображення сторінок з перемалюванням. Перемалювання викликається у фоні після переходу на іншу сторінку.

        Може викликати ефект, коли прив'язка скролінгу є на двох сторінках, то на одні сторінці після переходу з іншої
        буде не працювати скролінг. (Якщо не використовувати прив'язки, то буде працювати добре)

        Args:
            name (str): ім'я сторінки
            redraw_frame (bool): чи треба перемальовувати сторінку

        Raises:
            ValueError: Помилка, якщо немає зареєстрованого будівника для [name] типу сторінок
        """
        if name != self.__current_page:
            self._backgroud_redraw()
            if redraw_frame:
                self.__marked_for_redraw.append(name)
        
        if name not in self.__pages.keys():
            try: 
                self.page_builder(name)
            except Exception as e:
                raise ValueError(f'Cant show the Page for this name: {name}. Error msg: {e}')
        
        self._show_frame(name)
        
    def _show_page_without_back_redraw(self, name: str, redraw_frame: bool):
        """
        Метод відображення сторінок з перемалюванням. Перемалювання викликається одразу перед відкриттям сторінки.
        
        Цей метод не такий плавний, як _show_page() який використовує перемалювання у фоні, але від оптимально 
        працює з прив'язками скролінгу на linux

        Args:
            name (str): ім'я сторінки
            redraw_frame (bool): чи треба перемальовувати сторінку

        Raises:
            ValueError: Помилка, якщо немає зареєстрованого будівника для [name] типу сторінок
        """
        if name == self.__current_page:
            return
        else:
            if redraw_frame:
                self._on_opening_redraw(name)
        
        self._show_frame(name)
        
    def get_binding_from_page(self, name: str):
        if name in self.__pages.keys():
            return self.__pages.get(name).master
    
    def get_binding(self, name: str):
        if name in self.__pages.keys():
            return self.__binds[name]
            
    def show_page(self, name: str, redraw_frame: bool = False):
        #self._show_page(name, redraw_frame)
        self._show_page_without_back_redraw(name, redraw_frame)

    def create_and_go(self, name: str, page: Page, redraw_frame: bool = True):
        self.set_page(name, page)
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
    
    def init_pages(self, pages: list[str]):
        for name in pages:
            page = self.page_builder(name)
            self.add_page(name, page)

__page_manager = PageManager()

def get_page_manager():
    return __page_manager