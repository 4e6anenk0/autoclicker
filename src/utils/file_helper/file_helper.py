from pathlib import Path


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