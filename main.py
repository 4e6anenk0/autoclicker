from app import App
from src.settings.settings import get_settings


if __name__ == "__main__":

    settings = get_settings()
    app = App(settings=settings)
    app.async_mainloop()

