# -*- coding: utf-8 -*-
from reportportal_client import RPClient

from .client import Client
from reportportal_client.helpers import timestamp
from typing import  Any, Optional, Union



class Launcher:

    def __init__(self, project_name: str, client: Client):
        self.project_name = project_name
        self.__client = client
        self.rp_request = self.__client.request
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
            self.__id = self.get_launch_id_by_uuid()
        return self.__id

    @property
    def uuid(self) -> str:
        if not self.__uuid:
            raise RuntimeError("Launch is not initialised.")

        return self.__uuid

    @property
    def client(self) -> RPClient:
        if not self.__RPClient:
            raise RuntimeError("Client is not initialized.")

        return self.__RPClient

    def create_client(self, launch_uuid: str = None) -> None:
        self.__RPClient = self.__client.create_rpclient(project_name=self.project_name, launch_uuid=launch_uuid)

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
            _uuid = self.client.start_launch(
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
            self.client.finish_launch(
                end_time=end_time,
                status=status,
                attributes=attributes,
                **kwargs  
            )
            self.client.terminate()
            self.__id = None
            self.__uuid = None
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

    def get_info(self, uuid: str = None, cache: bool = True, ttl: int = None):
        _uuid = uuid or self.uuid
        if not _uuid:
            raise RuntimeError("Launch UUID is not set.")
        return self.rp_request.get_info(url_parts=self.__launch_url_parts, uuid=_uuid, cache=cache, ttl=ttl)

    def get_launch_id_by_uuid(self, uuid: str = None, cache: bool = True, ttl: int = None) -> int:
        self.__id = self.get_info(uuid=uuid, cache=cache, ttl=ttl)
        return self.__id.get('id') if self.__id else None

    def get_last_launch_uuid(self, launch_name: str, cache: bool = True, ttl: int = None) -> Optional[str]:
        uuids = self.get_uuids_by_name(launch_name=launch_name, cache=cache, ttl=ttl)
        # uuids.sort(key=lambda x: x.get('start_time'), reverse=True)
        return uuids[-1] if uuids else None

    def get_uuids_by_name(self, launch_name: str, status: str = None, cache: bool = False, ttl: int = None) -> list[str]:
        launches = self.get_launches(filter_by_name=launch_name, status=status, cache=cache, ttl=ttl)
        return [launch.get('uuid') for launch in launches]

    def get_launches(
            self,
            filter_by_name: str = None,
            status: str = None,
            page_size: int = 100,
            cache: bool = False,
            ttl: int = None,
            sort: str = "start_time,desc",
            **kwargs: Any
    ) -> list[dict]:
        return self.rp_request.get_items(
            self.url_parts,
            page_size=page_size,
            filter_by_name=filter_by_name,
            filter_by_status=status,
            sort=sort,
            cache=cache,
            ttl=ttl,
            **kwargs
        )
