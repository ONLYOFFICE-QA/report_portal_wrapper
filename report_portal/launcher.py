# -*- coding: utf-8 -*-
from reportportal_client import RPClient

from .client import Client
from reportportal_client.helpers import timestamp
from typing import  Any, Optional, Union



class Launcher:

    def __init__(self, project_name: str, client: Client):
        self.project_name = project_name
        self.auth = client
        self.__RPClient = None
        self.__id = None
        self.uuid = None
        self.__launch_url_parts = f"{self.project_name}/launch"
        self.__launch_connected: bool = False
        self.create_client()

    @property
    def id(self) -> int:
        if not self.__id:
            self.__id = self.get_launch_id_by_uuid()
        return self.__id

    @property
    def client(self) -> RPClient:
        if not self.__RPClient:
            raise RuntimeError("Client is not initialized.")

        return self.__RPClient

    def create_client(self, launch_uuid: str = None) -> None:
        self.__RPClient = self.auth.create(project_name=self.project_name, launch_uuid=launch_uuid)

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
            uuid = self.get_last_launch_uuid(launch_name=name) if last_launch_connect else None
            self.create_client(launch_uuid=uuid)

        try:
            self.uuid = self.client.start_launch(
                name=name,
                start_time=start_time,
                description=description,
                attributes=attributes,
                rerun=rerun,
                rerun_of=rerun_of,
                **kwargs
            )
            return self.uuid

        except Exception as e:
            raise RuntimeError(f"Failed to start launch '{name}': {e}")

    def get_launch_info(self, uuid: str = None):
        _uuid = uuid or self.uuid
        if not _uuid:
            raise RuntimeError("Launch UUID is not set.")

        return self.auth.request.get(f"{self.__launch_url_parts}/uuid/{_uuid}")

    def get_launch_id_by_uuid(self, uuid: str = None) -> int:
        self.__id = self.get_launch_info(uuid=uuid)
        return self.__id.get('id') if self.__id else None

    def get_last_launch_uuid(self, launch_name: str) -> Optional[str]:
        uuids = self.get_uuids_by_name(launch_name=launch_name)
        return uuids[-1] if uuids else None

    def get_uuids_by_name(
        self,
        launch_name: str,
        status: str = None,
        page: int = None,
        page_size: int = None
        ) -> list[str]:
        launches = self.get_launches_by_name(launch_name=launch_name, status=status, page=page, page_size=page_size)
        return [launch.get('uuid') for launch in launches]


    def get_launches_by_name(
            self,
            launch_name: str,
            status: str = None,
            page: int = None,
            page_size: int = None
    ) -> list[dict]:
        params = {
            "filter.eq.name": launch_name,
        }

        if status is not None:
            params["filter.eq.status"] = status

        if page is not None:
            params["page.page"] = page

        if page_size is not None:
            params["page.size"] = page_size

        return self.auth.request.get(self.__launch_url_parts, params=params).get("content", [])

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
            self.client.finish_launch(
                end_time=end_time,
                status=status,
                attributes=attributes,
                **kwargs  
            )
            self.client.terminate()
            self.id = None
            self.uuid = None
            self.__launch_connected = False
        except Exception as e:
            raise RuntimeError(f"Failed to finish launch '{self.id}': {e}")

        self.client.terminate()

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
            self.client.log(
                time=time,
                message=message,
                level=level,
                attachment=attachment,
                item_id=item_id,
                **kwargs  
            )
        except Exception as e:
            raise RuntimeError(f"Failed to send log to ReportPortal: {e}")

