# -*- coding: utf-8 -*-
from reportportal_client.helpers import timestamp
from typing import  Any, Optional, Union

from .client import Client
from .client.rp_client import RPClientAdvanced


class Launcher:
    """High-level API for managing ReportPortal launches.

    :param client: Configured client wrapper used to build RP client.
    """

    item_type = 'launch'

    def __init__(self, client: Client):
        """Initialize launcher instance.

        :param client: Configured client wrapper used to build RP client.
        """
        self.client = client
        self.__RPClient = None
        self.__id = None
        self.__uuid = None
        self.__launch_connected: bool = False
        self.create_client()

    @property
    def id(self) -> Union[str, int]:
        """Get launch ID, fetching it from ReportPortal if not cached.

        :return: Launch ID (string or integer).
        """
        if not self.__id:
            self.__id = self.get_launch_id_by_uuid(uuid=self.uuid)
        return self.__id

    @property
    def uuid(self) -> str:
        """Get launch UUID.

        :return: Launch UUID string.
        :raises RuntimeError: If launch is not initialized.
        """
        if not self.__uuid:
            raise RuntimeError("Launch is not initialised.")

        return self.__uuid

    @property
    def rp_client(self) -> RPClientAdvanced:
        """Get underlying ReportPortal client instance.

        :return: RPClientAdvanced instance.
        :raises RuntimeError: If client is not initialized.
        """
        if not self.__RPClient:
            raise RuntimeError("Client is not initialized.")

        return self.__RPClient

    def create_client(self, launch_uuid: str = None) -> None:
        """
        (Re)create underlying RP client.

        :param launch_uuid: Optional launch UUID to bind the client to.
        """
        self.__RPClient = self.client.create_rpclient(launch_uuid=launch_uuid)

    def connect(self, launch_uuid: str) -> None:
        """
        Connect to an existing launch by UUID.

        :param launch_uuid: Existing launch UUID to continue.
        """
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
        """
        Start a new launch or connect to the last one with the same name.

        :param name: Launch name.
        :param last_launch_connect: If True, attempt to connect to last launch with same name.
        :param start_time: Custom start time; default is current timestamp.
        :param description: Optional description.
        :param attributes: Optional attributes list or dict.
        :param rerun: Rerun flag.
        :param rerun_of: UUID of a launch to rerun.
        :return: Created launch UUID.
        """
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
        """Finish active launch and terminate client session.

        :param end_time: Custom end time; default is current timestamp.
        :param status: Final launch status.
        :param attributes: Optional attributes.
        """
        if self.__uuid is None:
            raise RuntimeError("No active launch to finish.")

        end_time = end_time or timestamp()
        attributes = attributes or {}

        self.rp_client.finish_launch(
            end_time=end_time,
            status=status,
            attributes=attributes,
            **kwargs
        )
        self.__id = None
        self.__uuid = None
        self.__launch_connected = False
        self.rp_client.terminate()

    def get_launch_id_by_uuid(self, uuid: str, cache: bool = True, ttl: int = None) -> str | None:
        """Get launch ID by UUID.

        :param uuid: Launch UUID.
        :param cache: Use cache.
        :param ttl: Cache TTL in seconds.
        :return: Launch ID or None.
        """
        return self.rp_client.get_id(item_type=self.item_type, uuid=uuid, cache=cache, ttl=ttl)

    def get_last_launch_uuid(self, by_name: str = None, cache: bool = True, ttl: int = None) -> Optional[str]:
        """Get the UUID of the last launch, optionally filtered by name.

        :param by_name: Filter by launch name.
        :param cache: Use cache.
        :param ttl: Cache TTL in seconds.
        :return: Launch UUID or None.
        """
        last_launch = self.get_last_launch(by_name=by_name, cache=cache, ttl=ttl)
        return last_launch.get('uuid') if last_launch else None

    def get_uuids_by_name(self, launch_name: str, status: str = None, cache: bool = False, ttl: int = None) -> list[str]:
        """Get all launch UUIDs by name and optional status.

        :param launch_name: Launch name to filter by.
        :param status: Optional status filter.
        :param cache: Use cache.
        :param ttl: Cache TTL in seconds.
        :return: List of UUID strings.
        """
        launches = self.get_launches(by_name=launch_name, status=status, cache=cache, ttl=ttl)
        return [launch.get('uuid') for launch in launches]

    def get_last_launch(self, by_name: str = None, status: str = None, cache: bool = True, ttl: int = None):
        """Get the last launch entity by optional filters.

        :param by_name: Optional name filter.
        :param status: Optional status filter.
        :param cache: Use cache.
        :param ttl: Cache TTL in seconds.
        :return: Launch dict or None.
        """
        launches = self.get_launches(by_name=by_name, status=status, cache=cache, ttl=ttl)
        return launches[-1] if launches else None

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
        """
        List launches with optional filters.

        :param by_name: Optional name filter.
        :param status: Optional status filter.
        :param page_size: Page size for pagination.
        :param cache: Use cache.
        :param ttl: Cache TTL in seconds.
        :param sort: Sort expression.
        :return: List of launch dictionaries.
        """
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
