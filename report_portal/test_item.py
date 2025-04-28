# -*- coding: utf-8 -*-
from reportportal_client.helpers import timestamp
from reportportal_client.core.rp_issues import Issue
from typing import Optional, Dict, Union, Any, Tuple

from .launcher import Launcher



class TestItem:

    def __init__(self, launcher: Launcher, item_type: str = "TEST"):
        self.item_type = item_type.upper()
        self.launcher = launcher
        self.__item_uuid = None
        self.__item_id = None
        self.url_parts = f"{self.launcher.project_name}/item"

    @property
    def id(self):
        if self.__item_id is None:
            self.__item_id = self.get_id(uuid=self.uuid)
        return self.__item_id

    @property
    def uuid(self):
        if not self.__item_uuid:
            raise RuntimeError(f"{self.item_type.lower()} item has not been started. Cannot finish the suite.")
        return self.__item_uuid

    def start(
            self,
            name: str,
            attributes: Optional[Dict[str, Any]] = None,
            description: Optional[str] = None,
            parameters: Optional[dict] = None,
            parent_item_id: Optional[str] = None,
            has_stats: bool = True,
            code_ref: Optional[str] = None,
            retry: bool = False,
            test_case_id: Optional[str] = None,
            retry_of: Optional[str] = None,
            uuid: Optional[str] = None,
            **kwargs: Any
    ) -> str:
        try:
            _item_uuid = self.launcher.client.start_test_item(
                name=name,
                start_time=timestamp(),
                item_type=self.item_type,
                description=description,
                attributes=attributes,
                parameters=parameters,
                parent_item_id=parent_item_id,
                has_stats=has_stats,
                code_ref=code_ref,
                retry=retry,
                test_case_id=test_case_id,
                retry_of=retry_of,
                uuid=uuid,
                **kwargs
            )
            self.__item_uuid = _item_uuid
            return _item_uuid

        except Exception as e:
            raise RuntimeError(f"Failed to start item '{name}': {e}")

    def finish(
            self,
            return_code: int,
            item_id: str = None,
            status: Optional[str] = None,
            issue: Optional[Issue] = None,
            attributes: Optional[Union[list, dict]] = None,
            description: Optional[str] = None,
            retry: Optional[bool] = False,
            test_case_id: Optional[str] = None,
            retry_of: Optional[str] = None,
            **kwargs: Any
    ):
        status = status or ("PASSED" if return_code == 0 else "FAILED")
        item_id = item_id or self.uuid

        if not item_id:
            raise RuntimeError("Test item has not been started. Cannot finish the test.")

        try:
            self.launcher.client.finish_test_item(
                item_id=item_id,
                end_time=timestamp(),
                status=status,
                issue=issue,
                attributes=attributes,
                description=description,
                retry=retry,
                test_case_id=test_case_id,
                retry_of=retry_of,
                **kwargs
            )

        except Exception as e:
            raise RuntimeError(f"Failed to finish test with item ID '{self.id}' in ReportPortal: {str(e)}")

    def update(
        self,
            item_uuid: str,
            attributes: Optional[Union[list, dict]] = None,
            description: Optional[str] = None
    ) -> Optional[str]:
        self.launcher.client.update_test_item(
            item_uuid=item_uuid,
            attributes=attributes,
            description=description
        )

    def send_log(
            self,
            message: str,
            item_id: Optional[str] = None,
            level: Union[int, str] = "INFO",
            attachment: Optional[dict] = None,
            **kwargs: Any
    ) -> Optional[Tuple[str, ...]]:

        valid_levels = ["INFO", "DEBUG", "WARN", "ERROR", "TRACE"]
        if isinstance(level, str) and level not in valid_levels:
            raise ValueError(f"Invalid log level: {level}. Must be one of {valid_levels}.")

        item_id = item_id or self.uuid

        if not item_id:
            raise RuntimeError("Cannot send log: No active test item. Start a test first.")

        try:
            return self.launcher.client.log(
                time=timestamp(),
                message=message,
                level=level,
                attachment=attachment,
                item_id=item_id,
                **kwargs
            )

        except Exception as e:
            raise RuntimeError(f"Failed to send log message to ReportPortal: {str(e)}")

    def get_info(self, uuid: str = None, cache: bool = True, ttl: int = None):
        return self.launcher.rp_request.get_info(
            url_parts=self.url_parts,
            uuid=uuid or self.uuid,
            cache=cache,
            ttl=ttl
        )

    def get_id(self, uuid: str, cache: bool = True, ttl: int = None):
        return self.launcher.rp_request.get_id(
            url_parts=self.url_parts,
            uuid=uuid,
            cache=cache,
            ttl=ttl
        )

    def get_items(self, page_size: int = 100, cache: bool = False, ttl: int = None) -> list[dict]:
        return self.launcher.rp_request.get_items(
            self.url_parts,
            filter_by_launch_id=self.launcher.id,
            page_size=page_size,
            cache=cache,
            ttl=ttl
        )

    def get_items_by_type(self, page_size: int = 100, cache: bool = False, ttl: int = None):
        return self.launcher.rp_request.get_items(
            self.url_parts,
            filter_by_launch_id=self.launcher.id,
            filter_by_type=self.item_type,
            page_size=page_size,
            cache=cache,
            ttl=ttl
        )
