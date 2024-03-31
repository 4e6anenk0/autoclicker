from enum import Enum
import logging
from pathlib import Path

from src.utils.file_helper.file_helper import create_destination_path


class Levels(Enum):
    
    notset = 'NOTSET'
    debug = 'DEBUG'
    Info = 'INFO'
    warning = 'WARNING'
    error = 'ERROR'
    critical = 'CRITICAL'

class Modes(Enum):
    
    '''
    Use [dev] setting for verbose console output, use [prod] setting for compact console output
    '''
    dev = 'dev'
    prod = 'prod'

class AppLogger:

    level = Levels.Info.value
    root_path = Path(__file__).parent.parent.parent.parent
    path_logfile = root_path.joinpath('data/logs/logs.txt')
    cli_mode = Modes.dev.value
    detail_cli_log_format = f"%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
    minimal_cli_log_format = f"%(asctime)s    [%(levelname)s] - %(message)s"

    @classmethod
    def _get_cli_log_format(cls):
        #mode = get_settings().get(Sections.project.value, 'mode')
        if cls.cli_mode == 'dev':
            return cls.detail_cli_log_format
        elif cls.cli_mode == 'prod':
            return cls.minimal_cli_log_format
        else:
            raise ValueError(f"Only [prod] and [dev] options are available. The following key option caused an exception: {cls.cli_mode}")
    
    @classmethod
    def _get_file_handler(cls):
        print(cls.root_path)
        print(cls.path_logfile)
        if not cls.path_logfile.exists():
            create_destination_path(cls.path_logfile)
        file_handler = logging.FileHandler(f'{cls.path_logfile}')
        file_handler.setLevel(logging.WARNING)
        file_handler.setFormatter(logging.Formatter(f"%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"))
        return file_handler

    @classmethod
    def _get_stream_handler(cls):  
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        stream_handler.setFormatter(logging.Formatter(cls._get_cli_log_format(), datefmt='%H:%M:%S'))
        return stream_handler

    @classmethod
    def get_logger(cls, name: str, use_filelog: bool = True, use_streamlog: bool = True):
        logger = logging.getLogger(name)
        logger.setLevel(cls.level)
        if use_filelog:
            logger.addHandler(cls._get_file_handler())
        if use_streamlog:
            logger.addHandler(cls._get_stream_handler())
        return logger