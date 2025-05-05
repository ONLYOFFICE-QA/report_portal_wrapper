# -*- coding: utf-8 -*-
import json
from pathlib import Path
from typing import Dict, Any


class Config:
    default_config_path = str(Path.home() / ".report_portal" / "config.json")

    def __init__(self, config_path: str = None):
        self.config_path = config_path or self.default_config_path
        self.__config = self._load_config(self.config_path)
        self.endpoint = self.__config['endpoint']
        self.api_key = self.__config['api_key']
        self.api_version = self.__config.get('api_version', None)

    def _load_config(self, json_path: str) -> Dict[str, Any]:
        """
        Loads the configuration from the JSON file.

        :return: Dictionary with configuration parameters.
        """
        try:
            with open(json_path, "r") as config_file:
                return json.load(config_file)

        except (FileNotFoundError, json.JSONDecodeError) as e:
            raise RuntimeError(f"Failed to load config from {self.config_path}: {e}")
