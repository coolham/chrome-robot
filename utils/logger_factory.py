# logger_factory.py
import os
import yaml
import logging
from utils.logger import Logger

_loggers = {}
_default_log_dir = None

def create_logger(log_prefix: str = 'app', log_level: str = 'info', log_dir: str = None):
    # Dictionary to store loggers for different prefixes
    global _loggers, _default_log_dir
    
     # 在第一次调用时设置默认log_dir
    if _default_log_dir is None and log_dir is not None:
        _default_log_dir = log_dir
    
    # 如果在后续调用中未指定log_dir，则使用默认值
    if log_dir is None:
        log_dir = _default_log_dir if _default_log_dir else 'logs'
        
    if not "_loggers" in globals():
        _loggers = {}

    if log_prefix not in _loggers:
        log_level_dict = {
            'CRITICAL': logging.CRITICAL,
            'ERROR': logging.ERROR,
            'WARNING': logging.WARNING,
            'INFO': logging.INFO,
            'DEBUG': logging.DEBUG
        }
        log_level_i = log_level_dict.get(log_level.upper(), logging.INFO)
        _loggers[log_prefix] = Logger(log_name=log_prefix, log_dir=log_dir, log_level=log_level_i).get_logger()

    return _loggers[log_prefix]
