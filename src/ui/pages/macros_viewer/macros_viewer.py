from typing import Any, Callable, Literal, Tuple
from customtkinter import CTkFrame, CTkButton, CTkScrollableFrame, CTkLabel, CTkImage
import threading 
import time

from src.clicker.models.macros import Macros
from src.clicker.models.macros_manager import MacrosManager
from src.settings.settings import Settings, Texts, get_settings
from src.ui.pages.page import Page, PageManager, Pages
from src.ui.pages.macros_editor.macros_editor import MacrosEditor
from src.utils.file_helper.file_helper import load_img


class MacrosViewer(Page):
    def __init__(self, master: Any, settings: Settings, macros_manager: MacrosManager, batch_size: int = 5, **kwargs):
        super().__init__(master, settings, **kwargs)    
        self.page_manager = PageManager()
        self.macros_manager = macros_manager
        self.macros_views: list[MacrosView] = []
        self.batch_size = batch_size
        self.batcher = self.macros_manager.load_macroses(batch_size)
        self.mode: Literal['selectable', 'view'] = 'view'
        self.selected_macroses: list[Macros] = []
        self.sources = {}

        self.create_content().pack_configure(fill='both', expand=True)
        
    def update_batcher(self):
        self.batcher = self.macros_manager.load_macroses(self.batch_size)

    def get_macroses(self):    
        try:
            macroses = next(self.batcher)
            print(macroses)
            if macroses:
                for macros in macroses:
                    if macros:
                        view = MacrosView(self.scrollable_content, macros=macros, viewer=self)
                        view.show()
                        self.macros_views.append(view)
        except:
            self.no_nodes_info.pack_configure(fill='x', expand=False, pady=30)

    def hide_all_macros_view(self):
        for view in self.macros_views:
            view.pack_forget()

    def create_content(self) -> Page:
        self.frame = CTkFrame(self)

        header = HeaderPanel(self.frame, manager=self.macros_manager, viewer=self)
        header.pack_configure(fill='both', expand=False)

        self.scrollable_content = CTkScrollableFrame(self.frame)
        self.scrollable_content.pack(fill='both', expand=True)

        self.no_nodes_info = CTkLabel(self.scrollable_content, text=get_settings().get_ui_text(Texts.macros_viewer_load_more_btn), anchor='n')

        # правильні прив'язки для роботи як в linux так і в windows
        # У Windows коліщатко миші прив’язується за допомогою <MouseWheel> методу, 
        # але для машини Linux прив’язка коліщатка миші призначена <Button-4>для прокручування вгору та <Button-5>
        self.scrollable_content.bind_all("<Button-4>", lambda e: self.scrollable_content._parent_canvas.yview("scroll", -1, "units"))
        self.scrollable_content.bind_all("<Button-5>", lambda e: self.scrollable_content._parent_canvas.yview("scroll", 1, "units"))

        self.page_nav = PageNavigator(self.frame, load_more_callback=self.get_macroses)
        self.page_nav.pack_configure(fill='x', expand=False, anchor='w')

        self.get_macroses()

        return self.frame
    

class PageNavigator(CTkFrame):
    def __init__(self, master: Any, load_more_callback: Callable, **kwargs):
        super().__init__(master, **kwargs)
        self.load_more_callback = load_more_callback

        self.create_content().pack_configure(fill='x', expand=False)

    def create_content(self):
        self.frame = CTkFrame(self)

        self.load_more_button = CTkButton(self.frame, text=get_settings().get_ui_text(Texts.macros_viewer_load_more_btn), command=self.load_more_callback, height=50)
        self.load_more_button.pack_configure(fill='x', expand=False)

        return self.frame

    
class MacrosView(CTkFrame):
    def __init__(self, master: Any, viewer: MacrosViewer, macros: Macros, **kwargs):
        super().__init__(master, **kwargs)
        self.viewer: MacrosViewer = viewer 
        self.macros: Macros = macros
        self.is_checked = False
        self.create_content().pack_configure(fill='both', expand=False)
        self.page_manager = PageManager()

    def create_content(self) -> CTkFrame:
        self.frame = CTkFrame(self, border_width=2, border_color='grey')

        if not self.viewer.sources.get('run_img'):
            run_img = load_img(get_settings().root_path.joinpath('src/icons/run.png'), resize=(40, 40))
            self.viewer.sources['run_img'] = run_img
        
        run_ctk_img = CTkImage(self.viewer.sources.get('run_img'), size=(30, 30))

        row = CTkFrame(self.frame, fg_color='transparent')
        row.grid_columnconfigure([1], weight=1)

        run_macros_button = CTkButton(row, 
                                      image=run_ctk_img, 
                                      text=get_settings().get_ui_text(Texts.macros_viewer_run_btn), 
                                      fg_color='transparent', 
                                      anchor='w', 
                                      command=self.run_script)
        run_macros_button.grid_configure(row=0, column=0, sticky='wns')
        
        text = f"{get_settings().get_ui_text(Texts.macros_viewer_label_text)}{self.macros.name}"
        label = CTkLabel(row, text=text, height=60, anchor='w')
        label.grid_configure(row=0, column=1, sticky='we', padx=10)
        label.bind("<Button-1>", self.on_click)

        row.pack_configure(fill='x', expand=True, padx=2, pady=2)
        
        return self.frame
    
    def run_script(self):
        time.sleep(2)
        #self.viewer.bind('<Escape>', lambda event: self.stop_script())
        self.thread = threading.Thread(target=self._run)
        self.thread.start()

    def _run(self):
        self.macros.run()

    # def stop_script(self, event):
    #     self.thread.join()
    #     print("The script was forced to stop")
    
    def show(self):
        self.pack_configure(fill='x', expand=False, pady=10, padx=10)

    def on_click(self, event):
        if self.viewer.mode == 'selectable':
            if not self.is_checked:
                self.check()
            else:
                self.uncheck()
        else:
            self.open_editor()
    
    def check(self):
        self.frame.configure(border_color='#1f6aa5')
        self.viewer.selected_macroses.append(self.macros)
        self.is_checked = True
        
    def uncheck(self):
        self.frame.configure(border_color='grey')
        self.viewer.selected_macroses.remove(self.macros)
        self.is_checked = False

    def open_editor(self):
        frame = self.page_manager.get_binding_from_page(Pages.macros_editor)
        page = MacrosEditor(frame, self.viewer.macros_manager, get_settings(), self.macros)
        
        self.page_manager.create_and_go(Pages.macros_editor, page)


class HeaderPanel(CTkFrame):
    def __init__(self, master: Any, viewer: MacrosViewer, manager: MacrosManager, **kwargs):
        super().__init__(master, **kwargs)
        self.viewer: MacrosViewer = viewer
        self.manager = manager
        self.page_manager = PageManager()

        self.create_content().pack_configure(fill='both', expand=False)

    def create_content(self) -> CTkFrame:
        self.frame = CTkFrame(self)
        self.frame.grid_configure(row=0, column=0)
        
        self.frame.grid_columnconfigure([1], weight=1)

        add_macros_button = CTkButton(self.frame, text=get_settings().get_ui_text(Texts.new_macros_btn), command=self.add_macros)
        add_macros_button.grid_configure(row=0, column=0, padx=10, pady=10, sticky='nws')

        right_frame = CTkFrame(self.frame, fg_color='transparent', bg_color='transparent')

        self.remove_button = CTkButton(right_frame, text=get_settings().get_ui_text(Texts.macros_viewer_remove_btn), fg_color='red', command=self.remove)

        """ remove_all_button = CTkButton(right_frame, text='Видалити все', fg_color='red', command=self.remove_all)
        remove_all_button.pack_configure(side='right', pady=10, padx=(5, 5)) """

        self.select_macroses_button = CTkButton(right_frame, text=get_settings().get_ui_text(Texts.macros_viewer_choose_btn), command= self.switch_mode)
        self.select_macroses_button.pack_configure(side='right', pady=10, padx=(10, 5))

        right_frame.grid_configure(row=0, column=1, sticky='nes')

        return self.frame
    
    def remove(self):
        if self.viewer.mode == 'selectable':
            for macros in self.viewer.selected_macroses:
                self.viewer.macros_manager.remove_macros(uuid=macros.uuid, localy=True)
                self.viewer.macros_manager.save_global_metadata()
            self.viewer.update_batcher()
            self.viewer.hide_all_macros_view()
            self.viewer.get_macroses()

    def uncheck_all(self):
        for view in self.viewer.macros_views:
            if view.is_checked:
                view.uncheck()
    
    def switch_mode(self):
        if self.viewer.mode == 'view':
            self.viewer.mode = 'selectable'
            self.remove_button.pack_configure(side='right', pady=10, padx=(5, 10))
            self.select_macroses_button.configure(text=get_settings().get_ui_text(Texts.macros_viewer_decline_btn), fg_color='red')
        else:
            self.viewer.mode = 'view'
            self.remove_button.pack_forget()
            self.uncheck_all()
            self.select_macroses_button.configure(text=get_settings().get_ui_text(Texts.macros_viewer_choose_btn), fg_color='#1f6aa5')

    def add_macros(self):
        frame = self.page_manager.get_binding_from_page(Pages.macros_editor)
        macros = Macros(self.manager.workdir)
        page = MacrosEditor(frame, self.manager, get_settings(), macros)
        
        self.page_manager.create_and_go(Pages.macros_editor, page)    
    
    def show_remove_btn(self):
        self.remove_button.pack_configure(side='right', pady=10, padx=(5, 5))

    def hide_remove_btn(self):
        self.remove_button.pack_forget()
    
    