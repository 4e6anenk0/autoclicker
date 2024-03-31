from app import App
from pynput.mouse import Button, Controller, Listener as MsListener
from pynput.keyboard import Key, Listener, Controller as KeyCon
from src.clicker.models.macros_manager import MacrosManager
from src.clicker.models.macros import Macros
from src.clicker.models.nodes.template_click_node import TemplateClickNode
from src.clicker.models.script import Script
from src.settings.settings import get_settings

from PIL import Image, ImageGrab

import tkinter as tk
from PIL import ImageGrab

def screenshot():
    # Отримання зображення екрана
    #image = ImageGrab.grab()
    #image.save("screenshot.png", "PNG")
    #window = tk.Tk()

    # Створення нового вікна для відображення зображення
    #screenshot_window = tk.Toplevel(window)
    #screenshot_window.title("Скріншот")

    # Додавання зображення до нового вікна
    #canvas = tk.Canvas(screenshot_window)
    #canvas.configure(background="black")
    #canvas.pack()
    #canvas.create_image(0, 0, image=image)

    # Створення прямокутників для виділення
    #start_x, start_y = None, None
    #rect = canvas.create_rectangle(0, 0, 0, 0, outline="yellow")

    #def on_mouse_move(event):
    #    global start_x, start_y
    #    if start_x is not None:
    #        canvas.coords(rect, start_x, start_y, event.x, event.y)

    #def on_mouse_down(event):
    #    global start_x, start_y
    #    start_x, start_y = event.x, event.y

    #canvas.bind("<Motion>", on_mouse_move)
    #canvas.bind("<Button-1>", on_mouse_down)

    window.mainloop()

""" def on_press(key: Key):
    if key is Key.esc:
        print(f'Зупинка')
        listener.stop()
    elif key is Key.alt_l:
        print(f'Текущее положение указателя: {mouse.position}')

def on_click(x: int, y: int, button: Button, passed: bool):
    if button is Button.right:
        print(f'Зупинка')
        listener.stop()
    elif button is Button.left:
        print(f'Текущее положение указателя: X: {x}, Y: {y}') """


if __name__ == "__main__":

    """ manager = MacrosManager(get_settings().macroses_path, get_settings().macroses_path.joinpath('metadata.json'))

    macros = Macros(get_settings().macroses_path)

    script = Script()
    script.add_node(TemplateClickNode(action='click', data='test/path/1'))
    script.insert_node(TemplateClickNode(action='click-after', data='test/path/2'), index=0, order='after')
    script.insert_node(TemplateClickNode(action='click-before', data='test/path/3'), index=1, order='before')

    macros.add_script(script)

    manager.add_macros(macros)

    manager.save_all_macroses() """

    """ manager.load_all_macroses()
    macroses = manager.get_all_macroses()
    for macros in macroses:
        print(macros)
        for node in macros.script.get_nodes():
            print(node) """

    """ manager = MacrosManager(get_settings().macroses_path, get_settings().macroses_path.joinpath('metadata.json'))
    print(manager)
    manager.load_all_macroses()

    macroses = manager.get_all_macroses()

    for _, macros in macroses:
        print(macros) """


    #script.save_script_to_file(get_settings().macroses_path.joinpath('new_script.json'))

    """ loaded_script = Script()
    loaded_script.load_script_from_file(get_settings().macroses_path.joinpath('new_script.json'))
    loaded_script.add_node(TemplateClickNode(action='new_action'))
    print(loaded_script) """
    #loaded_script.save_script_to_file(get_settings().macroses_path.joinpath('new_script.json'))
    



    settings = get_settings()
    app = App(settings=settings)
    app.async_mainloop()
    

    
    
    """ mouse = Controller()
    keyboard = KeyCon()
    
    listener = MsListener(on_click=on_click)
    
    listener.start()
    listener.join() """

    """ # Считывание положения указателя
    print(f'Текущее положение указателя: {mouse.position}')

    # Установка положения указателя
    #mouse.position = (10, 20)
    #print(f'Указатель перемещен в позицию: {mouse.position}')

    # Перемещение указателя относительно текущего положения
    new_pos = (mouse.position[0] + 10, mouse.position[1] - 10)
    print(f'New position is: {new_pos}')
    mouse.move(new_pos[0], new_pos[1])
    
    mouse.click(button=Button.right) """
