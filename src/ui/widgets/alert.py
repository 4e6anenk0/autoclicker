from customtkinter import CTkToplevel, CTkFrame, CTkLabel, CTkButton
from typing import Callable, Tuple

class Alert(CTkToplevel):
    def __init__(self, msg: str, confirm_btn_text: str, discard_btn_text: str, callback_confirm: Callable, callback_discard: Callable, screen_size: Tuple[int, int] = (400, 300), *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry(f"{screen_size[0]}x{screen_size[1]}")
        self.msg = msg
        self.confirm_btn_text = confirm_btn_text
        self.discard_btn_text = discard_btn_text

        self.resizable(False, False)

        self.create_content(callback_confirm, callback_discard).pack_configure(fill='both', expand=True)
    
    def create_content(self, callback_confirm, callback_discard):
        self.frame = CTkFrame(self)

        self.frame.columnconfigure([0,1], weight=1)
        
        label_frame = CTkFrame(self.frame, fg_color='transparent')

        label = CTkLabel(label_frame, text=self.msg)
        label.pack_configure(fill='x', expand=True)

        buttons_frame = CTkFrame(self.frame, fg_color='transparent')

        buttons_frame.columnconfigure([0,1], weight=1)

        confirm_button = CTkButton(buttons_frame, width=120, height=30, fg_color='green', command= lambda: callback_confirm(), text=self.confirm_btn_text)
        discard_button = CTkButton(buttons_frame, width=120, height=30, fg_color='red', command= lambda: callback_discard(), text=self.discard_btn_text)

        confirm_button.grid_configure(row=0, column=0, padx=(10, 5), pady=20)
        discard_button.grid_configure(row=0, column=1, padx=(5, 10), pady=20)

        label_frame.pack_configure(fill='both', expand=True)
        buttons_frame.pack_configure(fill='x', expand=True)

        return self.frame