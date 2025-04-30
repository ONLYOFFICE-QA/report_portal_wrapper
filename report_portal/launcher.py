# -*- coding: utf-8 -*-
from reportportal_client import RPClient

from .client import Client
from reportportal_client.helpers import timestamp
from typing import  Any, Optional, Union


class Launcher:

    def __init__(self, project_name: str, client: Client):
        self.project_name = project_name
        self.client = client
        self.request = self.client.rp_request.launch
        self.__RPClient = None
        self.__id = None
        self.__uuid = None
        self.__launch_url_parts = f"{self.project_name}/launch"
        self.__launch_connected: bool = False
        self.url_parts = f"{self.project_name}/launch"
        self.create_client()

    @property
    def id(self) -> int:
        if not self.__id:
            self.__id = self.request.get_launch_id_by_uuid(uuid=self.uuid)
        return self.__id

    @property
    def uuid(self) -> str:
        if not self.__uuid:
            raise RuntimeError("Launch is not initialised.")

        return self.__uuid

    @property
    def rp_client(self) -> RPClient:
        if not self.__RPClient:
            raise RuntimeError("Client is not initialized.")

        return self.__RPClient

    def create_client(self, launch_uuid: str = None) -> None:
        self.__RPClient = self.client.create_rpclient(launch_uuid=launch_uuid)

    def connect(self, launch_uuid: str):
        self.create_client(launch_uuid=launch_uuid)
        self.__launch_connected = True

    def start(
        self,
        name: str,
        last_launch_connect: bool = False,
        start_time: Optional[str] = None,
        description: Optional[str] = None, 
        attributes: Optional[list | dict] = None,
        rerun: bool = False,
        rerun_of: Optional[str] = None,
        **kwargs
    ) -> str:
        start_time = start_time or timestamp()
        attributes = attributes or {}

        if not self.__launch_connected:
            uuid = self.request.get_last_launch_uuid(by_name=name) if last_launch_connect else None
            self.create_client(launch_uuid=uuid)

        try:
            _uuid = self.rp_client.start_launch(
                name=name,
                start_time=start_time,
                description=description,
                attributes=attributes,
                rerun=rerun,
                rerun_of=rerun_of,
                **kwargs
            )
            self.__uuid = _uuid
            return _uuid

        except Exception as e:
            raise RuntimeError(f"Failed to start launch '{name}': {e}")

    def finish(
        self,
        end_time: Optional[str] = None,
        status: Optional[str] = "PASSED",
        attributes: Optional[Union[list, dict]] = None,
        **kwargs: Any
    ):
        if not self.uuid:
            raise RuntimeError("No active launch to finish.")

        end_time = end_time or timestamp() 
        attributes = attributes or {}

        try:
            self.rp_client.finish_launch(
                end_time=end_time,
                status=status,
                attributes=attributes,
                **kwargs  
            )
            self.rp_client.terminate()
            self.__id = None
            self.__uuid = None
            self.__launch_connected = False
        except Exception as e:
            raise RuntimeError(f"Failed to finish launch '{self.id}': {e}")

        self.rp_client.terminate()

    def send_log(
            self, 
            message: str, 
            level: Optional[Union[int, str]] = "INFO", 
            attachment: Optional[dict] = None, 
            item_id: Optional[str] = None,
            time: Optional[str] = None,
            print_output: bool = True,
            **kwargs: Any
        ):
        valid_levels = ["INFO", "DEBUG", "WARN", "ERROR", "TRACE"]
        if isinstance(level, str) and level not in valid_levels:
            raise ValueError(f"Invalid log level: {level}. Must be one of {valid_levels}.")

        if print_output:
            print(f"[{level}] {message}")

        if not self.id:
            raise RuntimeError("Cannot send log: No active launch. Please start a launch or connect to an existing one.")

        time = time or timestamp()  

        try:
            self.rp_client.log(
                time=time,
                message=message,
                level=level,
                attachment=attachment,
                item_id=item_id,
                **kwargs  
            )
        except Exception as e:
            raise RuntimeError(f"Failed to send log to ReportPortal: {e}")
