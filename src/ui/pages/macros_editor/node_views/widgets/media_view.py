from typing import Any
from customtkinter import CTkFrame, CTkImage, CTkLabel

class MediaView(CTkFrame):
    def __init__(self, master: Any, path_to_img: str = None, height: int = 200, **kwargs):
        super().__init__(master, **kwargs)
        self.path_to_img = path_to_img
        self.height = height

        self.create_content().pack_configure(fill='both', expand=True)
        
    def create_content(self) -> CTkFrame:
        self.frame = CTkFrame(self, fg_color='transparent', bg_color='transparent')

        if self.path_to_img:
            img = self.load_img(self.path_to_img, (150, 150))
            img_view = CTkImage(img, size = img.size)

            image_label = CTkLabel(self.frame, image=img_view, text="", height=self.height, width=self.height)
            
            image_label.grid_configure(row=0, column=0, padx=5, pady=5, sticky='nws')
        else:
            fill_label = CTkLabel(self.frame, text="No media", height=self.height, width=self.height)
            
            fill_label.grid_configure(row=0, column=0, padx=5, pady=5, sticky='nws')

        return self.frame