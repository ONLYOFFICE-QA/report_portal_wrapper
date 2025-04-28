# -*- coding: utf-8 -*-
from typing import Optional, Any

from .test_item import TestItemInfo
from .url_parts import UrlParts
from ..client import ReportPortalRequests


class LaunchInfo(TestItemInfo):

    def __init__(self, rp_requests: ReportPortalRequests, url_parts: UrlParts):
        super().__init__(rp_requests=rp_requests, url_parts=url_parts, item_type="TEST")
        self.url_parts = url_parts.launch

    def get_launch_id_by_uuid(self, uuid: str, cache: bool = True, ttl: int = None) -> str | None:
        return self.get_id(uuid=uuid, cache=cache, ttl=ttl)

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
        return self.rp_request.get_items(
            self.url_parts,
            page_size=page_size,
            filter_by_name=by_name,
            filter_by_status=status,
            sort=sort,
            cache=cache,
            ttl=ttl,
            **kwargs
        )

