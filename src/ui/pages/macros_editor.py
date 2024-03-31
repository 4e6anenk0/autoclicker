from typing import Any, Tuple
from customtkinter import CTkFrame, CTkLabel, CTkScrollableFrame, CTkOptionMenu, CTkFont

from src.clicker.models.nodes.node_factory import NodeName
from src.settings.settings import Settings, Texts
from src.ui.pages.page import ScrollablePage, Page


class MacrosEditor(Page):
    def __init__(self, master: Page, settings: Settings, **kwargs):
        super().__init__(master, settings, **kwargs)

        self.create_content().pack_configure(fill='both', expand=True)

    def create_content(self) -> CTkFrame:
        self.frame = CTkFrame(self)
        
        self.header = CTkFrame(self)
        self.header.pack_configure(fill='both', expand=False)
        
        self.scrollable_content = CTkScrollableFrame(self.frame)
        self.scrollable_content.pack(fill='both', expand=True)

        # правильні прив'язки для роботи як в linux так і в windows
        # У Windows коліщатко миші прив’язується за допомогою <MouseWheel> методу, 
        # але для машини Linux прив’язка коліщатка миші призначена <Button-4>для прокручування вгору та <Button-5>
        self.scrollable_content.bind_all("<Button-4>", lambda e: self.scrollable_content._parent_canvas.yview("scroll", -1, "units"))
        self.scrollable_content.bind_all("<Button-5>", lambda e: self.scrollable_content._parent_canvas.yview("scroll", 1, "units"))
        
        text = self.settings.get_ui_text(Texts.home_page_label)
        title = CTkLabel(self.header, text=text, font=CTkFont(size=20, weight='bold'))
        
        title.pack_configure(padx=16, pady=16, anchor='w')

        header_panel = HeaderPanel(self.header)
        header_panel.pack_configure(anchor='w')
        
        body_text = CTkLabel(self.scrollable_content, text='Test body text 1', font=CTkFont(size=20, weight='bold'))
        body_text.pack_configure(anchor='w')
        
        for _ in range(7):
            node_view = NodeView(self.scrollable_content)
            node_view.pack_configure(fill='x', padx=10, pady=10)

        
        
        return self.frame
    


    
class HeaderPanel(CTkFrame):
    def __init__(self, master: Any, **kwargs):
        super().__init__(master, **kwargs)
        self.nodes: NodeName = ['TemplateClickNode', 'ClickNode']

        self.create_content().pack_configure(fill='both', expand=False)

    def create_content(self) -> CTkFrame:
        self.frame = CTkFrame(self)
        self.frame.grid_configure(row=0, column=0)
        type_node_menu = CTkOptionMenu(self.frame, values=self.nodes)
        type_node_menu.grid_configure(row=0, column=0, padx=10, pady=10)
        type_node_menu.set('Type of node:')

        return self.frame


class NodeView(CTkFrame):
    def __init__(self, master: Any, height: int = 200, color: str = '#443742', **kwargs):
        super().__init__(master, **kwargs)
        self.height = height
        self.color = color
        self.create_content().pack_configure(fill='both', expand=False)

    def create_content(self) -> CTkFrame:
        self.frame = CTkFrame(self, height=self.height, fg_color=self.color, corner_radius=100)

        return self.frame