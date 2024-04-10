from pathlib import Path
from typing import Any, Callable, Tuple
from customtkinter import CTkFrame, CTkImage, CTkLabel, CTkButton, CTkFont
from PIL.Image import Image

from src.utils.file_helper.file_helper import load_img, resize_img, save_img
from src.ui.widgets.screenshot_action import ScreenshotAction

class MediaView(CTkFrame):
    def __init__(self, master: Any, node_view: Any, path_to_img: str = None, height: int = 200, is_selectable: bool = False, **kwargs):
        super().__init__(master, **kwargs)
        self.path_to_img = path_to_img
        self.height = height
        self.is_selectable = is_selectable
        self.node_view = node_view
        self.create_content().pack_configure(fill='both', expand=True)

    
        

    """ def sender(self):
        return self.action.screenshot """
        
    def create_content(self) -> CTkFrame:
        self.frame = CTkFrame(self)

        if self.path_to_img:
            img = load_img(self.path_to_img, (150, 150))
            img_view = CTkImage(img, size = img.size)

            self.image_label = CTkLabel(self.frame, image=img_view, text="", height=self.height, width=self.height)
            
            self.image_label.grid_configure(row=0, column=0, padx=5, pady=5, sticky='nws')
        else:
            if self.is_selectable:
                self.image_label = ScreenshotInput(self.frame, height=self.height, width=self.height, path_to_img=self.path_to_img, node_view=self.node_view)
                self.image_label.grid_configure(row=0, column=0, padx=5, pady=5, sticky='nws')
            else:
                fill_label = CTkLabel(self.frame, text="No media", height=self.height, width=self.height)
            
                fill_label.grid_configure(row=0, column=0, padx=5, pady=5, sticky='nws')

        return self.frame
    

class ScreenshotInput(CTkFrame):
    def __init__(self, master, height: str, width: str, node_view: Any, path_to_img: str, **kwargs):
        super().__init__(master, **kwargs)
        self.node_view = node_view
        self.height = height
        self.width = width
        self.path_to_img = path_to_img

        self.create_content().pack_configure(fill='both', expand=True)

    def create_content(self):
        self.frame = CTkFrame(self)

        self.button = CTkButton(self.frame, fg_color='transparent', hover_color='green', text='+', font=CTkFont(size=20, weight='bold'), command=self.show_screenshot_action, width=self.width, height=self.height)
        self.button.pack_configure(fill='both', expand=True)
        
        return self.frame
    
    def show_screenshot_action(self):
        self.action = ScreenshotAction(self.master, lambda img: self.after_screenshot_action(img))
        self.action.bind('<Escape>', lambda event: self.action.destroy())
        self.action.mainloop()
    
    def after_screenshot_action(self, img):
        self.node_view.img = img
        resized_img = resize_img(img, (150, 150))
        #save_img(img, path=self.path_to_img, name=self.node_id)
        #self.save_callback(resized_img)
        self.node_view.rimg = resize_img
        img_view = CTkImage(resized_img, size = resized_img.size)

        image_label = CTkLabel(self.frame, image=img_view, text="", height=self.height, width=self.height)
        self.button.pack_forget()

        image_label.pack_configure(fill='both', expand=True)