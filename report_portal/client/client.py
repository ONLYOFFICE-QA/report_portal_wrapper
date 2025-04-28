# -*- coding: utf-8 -*-
import json
from os.path import join, expanduser
from typing import Dict, Any

from reportportal_client import RPClient

from .config import Config
from .report_portal_requests import ReportPortalRequests


class Client:
    def __init__(self, config_path: str = None):
        self.config_path = config_path or join(expanduser('~'), ".report_portal", "config.json")
        self.config = Config()
        self.request = ReportPortalRequests(config=self.config)
        self.client = None

    def create_rpclient(self, project_name: str, launch_uuid: str | None = None):
        """
        Creates an instance of RPClient with merged configuration.
        """
        self.client = RPClient(
            endpoint=self.config.endpoint,
            project=project_name,
            api_key=self.config.api_key,
            launch_uuid=launch_uuid,
        )

        return self.client

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
