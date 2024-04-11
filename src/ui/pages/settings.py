from typing import Any, Callable, Protocol, Union
from customtkinter import CTkFrame, CTkLabel, CTkFont, CTkComboBox

from src.settings.settings import Langs, Sections, Settings, Texts
from src.ui.pages.page import Page


class SettingsPage(Page):
    def __init__(self, update_callback, master: Any, settings: Settings, **kwargs):
        super().__init__(master, settings, **kwargs)
        self.update_callback = update_callback
        self.create_content().pack_configure(fill='both', expand=False)

    def create_content(self) -> Page:
        self.frame = CTkFrame(self)
        
        text = self.settings.get_ui_text(Texts.settings_page_label)
        title = CTkLabel(self.frame, text=text, font=CTkFont(size=20, weight='bold'))

        title.pack_configure(padx=16, pady=16, anchor='w')

        field1 = SettingsComboBox(self.frame,
                                  command=self.on_choise_lang,
                                  label_text=self.settings.get_ui_text(Texts.settings_page_lang_field), 
                                  values=Langs.list(), 
                                  combobox_width=100)
        field1.set_value(self.settings.get(Sections.localization.value, 'lang'))
        field1.pack_configure(padx=10, pady=10, anchor='w')
        
        return self.frame
    
    def on_choise_lang(self, choise: str):
        self.settings.update_locale(choise)
        #self.mainframe.update_all()
        self.update_callback()
    

class SettingsComboBox(CTkFrame):
    def __init__(self, 
                 master: Any, 
                 label_text: str, 
                 values: list[str],
                 command: Union[Callable[[str], Any], None] = None, 
                 combobox_width: int = 140, 
                 **kwargs):
        super().__init__(master, **kwargs)
        self.text = label_text
        self.values = values
        self.width = combobox_width
        self.command = command

        self.create_content().pack_configure(fill='both', expand=False)

    def create_content(self):
        self.frame = CTkFrame(self)

        label = CTkLabel(self.frame, text=self.text)
        self.combobox = CTkComboBox(self.frame, values=self.values, state='readonly', width=self.width, command=lambda choise: self.command(choise))
        
        label.grid_configure(row=0, column=0, padx=(0, 40))
        self.combobox.grid_configure(row=0, column=1)

        return self.frame
    
    def set_value(self, value: str):
        self.combobox.set(value)