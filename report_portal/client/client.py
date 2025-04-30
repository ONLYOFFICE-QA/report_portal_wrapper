# -*- coding: utf-8 -*-
import json
from os.path import join, expanduser
from typing import Dict, Any

from .RPClient_advanced import RPClientAdvanced
from .config import Config
from .rp_requests import RpRequests, UrlParts


class Client:
    def __init__(self, project_name: str, config_path: str = None):
        self.config_path = config_path or join(expanduser('~'), ".report_portal", "config.json")
        self.project_name = project_name
        self.config = Config()
        self.url_parts = UrlParts(project_name=self.project_name)
        self.rp_request = RpRequests(config=self.config, url_parts=self.url_parts)
        self.rp_client = None
        self.create_rpclient()

    def create_rpclient(self, launch_uuid: str | None = None):
        """
        Creates an instance of RPClient with merged configuration.
        """
        self.rp_client = RPClientAdvanced(
            endpoint=self.config.endpoint,
            project=self.project_name,
            api_key=self.config.api_key,
            launch_uuid=launch_uuid,
        )
        return self.rp_client

    def _load_config(self) -> Dict[str, Any]:
        """
        Loads the configuration from the JSON file.

        :return: Dictionary with configuration parameters.
        """
        try:
            with open(self.config_path, "r") as config_file:
                return json.load(config_file)

        except (FileNotFoundError, json.JSONDecodeError) as e:
            raise RuntimeError(f"Failed to load config from {self.config_path}: {e}")
