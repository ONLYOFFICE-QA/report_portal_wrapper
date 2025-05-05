# -*- coding: utf-8 -*-
from reportportal_client.helpers import timestamp
from typing import  Any, Optional, Union

from .client import Client
from .client.rp_client import RPClientAdvanced


class Launcher:
    item_type = 'launch'

    def __init__(self, project_name: str, client: Client):
        self.project_name = project_name
        self.client = client
        self.__RPClient = None
        self.__id = None
        self.__uuid = None
        self.__launch_connected: bool = False
        self.create_client()

    @property
    def id(self) -> int:
        if not self.__id:
            self.__id = self.get_launch_id_by_uuid(uuid=self.uuid)
        return self.__id

    @property
    def uuid(self) -> str:
        if not self.__uuid:
            raise RuntimeError("Launch is not initialised.")

        return self.__uuid

    @property
    def rp_client(self) -> RPClientAdvanced:
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
            uuid = self.get_last_launch_uuid(by_name=name) if last_launch_connect else None
            self.create_client(launch_uuid=uuid)

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

        self.rp_client.terminate()

    def get_launch_id_by_uuid(self, uuid: str, cache: bool = True, ttl: int = None) -> str | None:
        return self.rp_client.get_id(item_type=self.item_type, uuid=uuid, cache=cache, ttl=ttl)

    def get_last_launch_uuid(self, by_name: str = None, cache: bool = True, ttl: int = None) -> Optional[str]:
        last_launch = self.get_last_launch(by_name=by_name, cache=cache, ttl=ttl)
        return last_launch.get('uuid') if last_launch else None

    def get_uuids_by_name(self, launch_name: str, status: str = None, cache: bool = False, ttl: int = None) -> list[str]:
        launches = self.get_launches(by_name=launch_name, status=status, cache=cache, ttl=ttl)
        return [launch.get('uuid') for launch in launches]

    def get_last_launch(self, by_name: str = None, status: str = None, cache: bool = True, ttl: int = None):
        launches = self.get_launches(by_name=by_name, status=status, cache=cache, ttl=ttl)
        return launches[-1] if launches else []

    def get_launches(
            self,
            by_name: str = None,
            status: str = None,
            page_size: int = 100,
            cache: bool = False,
            ttl: int = None,
            sort: str = "start_time,desc",
            **kwargs: Any
    ) -> list[dict]:
        return self.rp_client.get_items(
            item_type=self.item_type,
            page_size=page_size,
            filter_by_name=by_name,
            filter_by_status=status,
            sort=sort,
            cache=cache,
            ttl=ttl,
            **kwargs
        )
