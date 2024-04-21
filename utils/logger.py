import os
import logging
from logging.handlers import TimedRotatingFileHandler
import time
import datetime


# Modifying the Logger class to ensure all log messages are written to the same file

class Logger(object):
    # Static variable to store the common file handler
    _file_handler = None

    def __init__(self, log_name='app', log_dir='logs', log_level=logging.INFO):
        # Use a fixed log file name
        now_str = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        if not os.path.exists(log_dir):
            os.mkdir(log_dir)
        log_file = f'biopsy_{now_str}.log'
        log_file = os.path.join(log_dir, log_file)
            
        # 创建logger
        self.logger = logging.getLogger(log_name)
        self.logger.setLevel(log_level)

        if not Logger._file_handler:
            # Create the common FileHandler if it doesn't exist
            Logger._file_handler = logging.handlers.TimedRotatingFileHandler(log_file, when='D', interval=1,
                                                                             backupCount=30, encoding='utf-8')
            formatter_fh = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(name)s - [ %(message)s ] - %(filename)s - %(funcName)s:%(lineno)d')
            Logger._file_handler.setFormatter(formatter_fh)

        # Use the common FileHandler
        self.logger.addHandler(Logger._file_handler)

        # 创建一个StreamHandler,输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(log_level)
        formatter_ch = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(name)s - [ %(message)s ] - %(filename)s - %(funcName)s:%(lineno)d')
        ch.setFormatter(formatter_ch)

        # 添加StreamHandler
        self.logger.addHandler(ch)

    def get_logger(self):
        return self.logger
    
    def set_level(self, log_level):
        log_level_dict = {
            'CRITICAL': logging.CRITICAL,
            'ERROR': logging.ERROR,
            'WARNING': logging.WARNING,
            'INFO': logging.INFO,
            'DEBUG': logging.DEBUG
        }
        log_level_i = log_level_dict.get(log_level.upper(), logging.INFO)
        self.logger.setLevel(log_level_i)


def test():
    # Testing the modified Logger class
    logger1 = Logger(log_level=logging.DEBUG).get_logger()
    logger2 = Logger(log_level=logging.ERROR).get_logger()

    # Logging some test messages
    logger1.debug("This is a debug message from logger1")
    logger2.error("This is an error message from logger2")
