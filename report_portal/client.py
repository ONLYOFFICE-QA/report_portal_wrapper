# -*- coding: utf-8 -*-
import json
from os.path import join, expanduser
from typing import Dict, Any

from reportportal_client import RPClient


class Client:
    def __init__(self, config_path: str = None):
        self.config_path = config_path or join(expanduser('~'), ".report_portal", "config.json")
        self.client = None

    def create(self, project_name: str, launch_uuid: str | None = None):
        """
        Creates an instance of RPClient with merged configuration.
        """
        config = self._load_config()
        self.client = RPClient(
            endpoint=config["endpoint"],
            project=project_name,
            api_key=config["api_key"],
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

    def get(self):
        """
        Retrieves the initialized ReportPortal client.

        :raises RuntimeError: If the client is not initialized.
        :return: The initialized RPClient instance.
        """
        if not self.client:
            raise RuntimeError("Client is not initialized.")

        return self.client


