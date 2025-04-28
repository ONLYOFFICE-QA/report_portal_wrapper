# -*- coding: utf-8 -*-
from .test_item import TestItemInfo
from .url_parts import UrlParts
from ..client import ReportPortalRequests


class TestInfo(TestItemInfo):

    def __init__(self, rp_requests: ReportPortalRequests, url_parts: UrlParts):
        super().__init__(rp_requests=rp_requests, url_parts=url_parts, item_type="TEST")

    def get_tests(
            self,
            launch_id: str,
            page_size: int = 100,
            cache: bool = False,
            ttl: int = None
    ) -> list[dict]:
        return self.get_items(
            filter_by_launch_id=launch_id,
            filter_by_type=self.item_type,
            page_size=page_size,
            cache=cache,
            ttl=ttl
        )

    def get_tests_by_name(
            self,
            launch_id: str,
            name: str,
            page_size: int = 100,
            cache: bool = False,
            ttl: int = None
    ) -> list[dict]:
        return self.get_items(launch_id=launch_id, filter_by_name=name, page_size=page_size, cache=cache, ttl=ttl)

