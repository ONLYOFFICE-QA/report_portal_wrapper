# -*- coding: utf-8 -*-
from .rp_client import RPClientAdvanced
from .config import Config


class Client:

    def __init__(self, project_name: str, config_path: str = None):
        self.project_name = project_name
        self.config = Config(config_path=config_path)
        self.__rp_client = None
        self.create_rpclient()

    @property
    def rp_client(self):
        if self.__rp_client is None:
            raise RuntimeError("Client is not initialized.")

        return self.__rp_client

    def create_rpclient(self, launch_uuid: str | None = None):
        """
        Creates an instance of RPClient with merged configuration.
        """
        self.__rp_client = RPClientAdvanced(
            config=self.config,
            project_name=self.project_name,
            launch_uuid=launch_uuid
        )

        return self.__rp_client
