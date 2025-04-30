# -*- coding: utf-8 -*-
from .url_parts import UrlParts
from .report_portal_requests import ReportPortalRequests


class TestItem:

    def __init__(self, rp_requests: ReportPortalRequests, url_parts: UrlParts, item_type: str = "TEST", launch_id: str = None):
        self.request = rp_requests
        self.url_parts = url_parts.test_item
        self.item_type = item_type.upper()
        self.launch_id = launch_id

    def get_info(self, uuid: str, cache: bool = True, ttl: int = None):
        return self.request.get_info(
            url_parts=self.url_parts,
            uuid=uuid,
            cache=cache,
            ttl=ttl
        )

    def get_id(self, uuid: str, cache: bool = True, ttl: int = None):
        return self.request.get_id(
            url_parts=self.url_parts,
            uuid=uuid,
            cache=cache,
            ttl=ttl
        )

    def get_items(self, launch_id: str = None, **kwargs: any) -> list[dict]:
        return self.request.get_items(launch_id=launch_id or self.launch_id, url_parts=self.url_parts, **kwargs)

    def get_items_by_type(self, launch_id: str = None, **kwargs: any) -> list[dict]:
        return self.get_items(
            launch_id=launch_id,
            url_parts=self.url_parts,
            filter_by_type=self.item_type,
            **kwargs)
