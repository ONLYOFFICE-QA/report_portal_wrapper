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
        self.request = launcher.client.rp_client.requests

    @property
    def id(self):
        if self.__item_id is None:
            self.__item_id = self.request.get_id(uuid=self.uuid)
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
            _item_uuid = self.launcher.rp_client.start_test_item(
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
            self.launcher.rp_client.finish_test_item(
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
            description: Optional[str] = None,
            status: Optional[str] = None,
            **kwargs: Any
    ) -> Optional[str]:

        _status = status.upper() if status else None

        if _status not in ["PASSED", "FAILED", "SKIPPED", 'IN_PROGRESS']:
            raise ValueError(f"Invalid status: {_status}. Must be one of ['PASSED', 'FAILED', 'SKIPPED'].")

        self.launcher.rp_client.update_test_item(
            item_uuid=item_uuid,
            attributes=attributes,
            description=description,
            status=_status,
            **kwargs
        )

    def send_log(
            self,
            message: str,
            item_uuid: Optional[str] = None,
            level: Union[int, str] = "INFO",
            print_output: bool = False,
            time: Optional[str] = None,
            attachment: Optional[dict] = None,
    ) -> Optional[Tuple[str, ...]]:

        valid_levels = ["INFO", "DEBUG", "WARN", "ERROR", "TRACE"]
        if isinstance(level, str) and level not in valid_levels:
            raise ValueError(f"Invalid log level: {level}. Must be one of {valid_levels}.")

        item_uuid = item_uuid or self.uuid

        if not item_uuid:
            raise RuntimeError("Cannot send log: No active test item. Start a test first.")

        if print_output:
            print(f"[{level}] {message}")

        return self.launcher.rp_client.send_log(
                message=message,
                launch_uuid=self.launcher.uuid,
                time=time or timestamp(),
                level=level,
                item_uuid=item_uuid
            )

    def get_info(self, uuid: str, cache: bool = True, ttl: int = None):
        return self.launcher.rp_client.get_info(
            item_type=self.item_type,
            uuid=uuid,
            cache=cache,
            ttl=ttl
        )

    def get_id(self, uuid: str, cache: bool = True, ttl: int = None):
        return self.launcher.rp_client.get_info(
            item_type=self.item_type,
            uuid=uuid,
            cache=cache,
            ttl=ttl
        )

    def get_items(self, launch_id: str = None, **kwargs: any) -> list[dict]:
        return self.launcher.rp_client.get_items(
            item_type=self.item_type,
            launch_id=launch_id or self.launcher.id,
            **kwargs
        )

    def get_items_by_type(self, launch_id: str = None, **kwargs: any) -> list[dict]:
        return self.get_items(
            launch_id=launch_id,
            filter_by_type=self.item_type,
            **kwargs
        )
