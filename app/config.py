import os
from pathlib import Path
import tomllib

class Config:
    _instance = None
    _config = None

    def __new__(cls): # one instance
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._config is None:
            self._load_config()

    def _load_config(self):
        path = Path(os.getenv("HACKANOMOUS_CONFIG_FILE", "./config.toml"))
        with open(path, "rb") as f:
            self._config = tomllib.load(f)

    def get(self, key: str, default=None) -> str | None:
        keys = key.split(".")
        value = self._config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        return value if value is not None else default

# global instance
config = Config()