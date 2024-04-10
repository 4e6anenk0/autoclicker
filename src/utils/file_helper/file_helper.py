from pathlib import Path
from typing import Tuple
from PIL import Image

def create_destination_dir(destination_path: str) -> bool:
    """
    Перевіряє чи є шлях, та створює у разі відсутності шлях, переданий
    в аргументі у вигляді строки.

    Args:
        destination_path (str): шлях що треба створити

    Returns:
        bool: True, якщо шлях був створений, False - якщо шлях вже існує
    """
    path = Path(destination_path)
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
        return True
    else:
        return False

def create_destination_path(destination_path: str) -> bool:
    """
    Перевіряє чи є шлях, та створює його у разі відсутності та файл, 
    що вказані в агрументі у вигляді переданої строки.

    Args:
        destination_path (str): шлях до файлу у вигляді строки

    Returns:
        bool: True якщо файл та шлях створені, інакше False
    """
    path = Path(destination_path)
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True) 
        Path.touch(destination_path)
        return True
    else:
        return False
    
def load_img(path: str, resize: Tuple[int, int] = None):
        img = Image.open(path)
        if resize:
            return resize_img(img, resize)
        return img

def save_img(img: Image.Image, path: str, name: str):
    path = Path(path, name)
    img.save(path, "png")

def resize_img(img: Image.Image, size: Tuple[int, int]):
        (current_width, current_height) = img.size
        (max_width, max_height) = size

        if current_width > max_width or current_height > max_height:
            if current_width / max_width > current_height / max_height:
                new_width = max_width
                new_height = int(current_height * (new_width / current_width))
            else:
                new_height = max_height
                new_width = int(current_width * (new_height / current_height))
        else:
            new_width = current_width
            new_height = current_height
            
        resized_img = img.resize((new_width, new_height))

        return resized_img