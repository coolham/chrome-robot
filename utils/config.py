import os
import yaml


class MasterConfig:
    _instance = None
    _config_loaded = False

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            if kwargs.get('config_file'):
                cls._instance.config_file = kwargs.get('config_file')
            else:
                cls._instance.config_file = None
            cls._instance.config = cls._instance.load_config()
            cls._config_loaded = True
        return cls._instance

    def __init__(self, *args, **kwargs):
        if not self._config_loaded:
            self.config_file = None
            self.config = self.load_config()

    def load_config(self):
        if not self.config_file:
            root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.config_file = os.path.join(root_dir, 'conf', 'config.yaml')
        try:
            with open(self.config_file, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            raise Exception(f"Configuration file {self.config_file} not found!")

    def get_config_obj(self):
        return self.config

    def get_config(self, section, *keys, default=None):
        dict_ = self.config
        if not dict_:
            return default
        
        keys = [section] + list(keys)
        for key in keys:
            dict_ = dict_.get(key, {})
            if dict_ is None or dict_ == {}:
                return default
        
        return dict_
    
    
    