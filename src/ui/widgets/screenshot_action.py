from pathlib import Path
from tkinter import Event
from typing import Any, Callable
from PIL import ImageGrab
from PIL.Image import Image
from customtkinter import CTkFrame, CTk, CTkToplevel, CTkCanvas
from src.settings.settings import Settings
from src.ui.pages.page import Page

        
class ScreenshotAction(CTkToplevel):
    def __init__(self, master, after_screenshot: Callable[[Image], Any] = lambda img: None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.after_screenshot = after_screenshot
        self.screen_size = (self.winfo_screenwidth(), self.winfo_screenheight())
        
        self.resizable(False, False)
        self.wm_attributes('-type', 'splash')
        self.geometry(f'{self.screen_size[0]}x{self.screen_size[1]}')
        self.wait_visibility(self)
        self.attributes('-alpha', 0.3)
        self.attributes('-topmost', 1)

        self.screenshot = None

        self.start_x = None
        self.start_y = None
        
        self.create_content().pack_configure(fill='both', expand=False)
        
        self.focus()



    def draw_rectangle(self, event):
        self.canvas.delete('all')

        if self.start_x == None:
            self.start_x = event.x
            self.start_y = event.y
            
        self.end_x = event.x
        self.end_y = event.y

        self.canvas.create_rectangle(self.start_x, self.start_y, self.end_x, self.end_y, fill='red')

            #print("Draw rectangle")

        """ self.start_x = None
        self.start_y = None """


    def make_screenshot(self, event):
        self.canvas.create_rectangle(self.start_x, self.start_y, self.end_x, self.end_y, fill='red')
        
        left_x, top_y, right_x, bottom_y = (self.start_x, self.start_y, self.end_x, self.end_y)

        self.start_x = None
        self.start_y = None

        self.forget(self)
    
        screenshot = ImageGrab.grab(bbox=(left_x, top_y, right_x, bottom_y))
        #screenshot.save("screenshot.png", "PNG")
        #print("MakeScreen")
        #return screenshot
        self.screenshot = screenshot
        
        self.after_screenshot(screenshot)
        
        self.destroy()


    def create_content(self) -> CTkCanvas:
        self.canvas = CTkCanvas(self, height = self.screen_size[1], width = self.screen_size[0], background='#000000')
        #self.canvas.create_oval(4000, 900, 500, 2500, fill='red')
        self.canvas.bind('<B1-Motion>', self.draw_rectangle)
        self.canvas.bind('<ButtonRelease-1>', self.make_screenshot)
        
        #self.canvas.pack_configure()

        return self.canvas
        

""" class SelectionRectangle:
    def __init__(self):
        start_x: int
        start_y: int


    def draw(self, ) """
