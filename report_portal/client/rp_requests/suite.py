# -*- coding: utf-8 -*-
from .report_portal_requests import ReportPortalRequests
from .test_item import TestItem
from .url_parts import UrlParts


class Suite(TestItem):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, item_type="SUITE", **kwargs)

    def get_suites(self, launch_id: str, page_size: int = 100, cache: bool = False, ttl: int = None) -> list[dict]:
        return self.request.get_items(
            self.url_parts,
            launch_id=launch_id,
            filter_by_type=self.item_type,
            page_size=page_size,
            cache=cache,
            ttl=ttl
        )
