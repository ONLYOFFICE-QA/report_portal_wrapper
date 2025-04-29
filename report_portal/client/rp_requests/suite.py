# -*- coding: utf-8 -*-
from .report_portal_requests import ReportPortalRequests
from .test_item import TestItemInfo
from .url_parts import UrlParts


class SuiteInfo(TestItemInfo):

    def __init__(self, rp_requests: ReportPortalRequests, url_parts: UrlParts):
        super().__init__(rp_requests=rp_requests, url_parts=url_parts, item_type="SUITE")

    def get_suites(self, launch_id: str, page_size: int = 100, cache: bool = False, ttl: int = None) -> list[dict]:
        return self.request.get_items(
            self.url_parts,
            filter_by_launch_id=launch_id,
            filter_by_type=self.item_type,
            page_size=page_size,
            cache=cache,
            ttl=ttl
        )
