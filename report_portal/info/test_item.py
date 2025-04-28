# -*- coding: utf-8 -*-
from .url_parts import UrlParts
from ..client import ReportPortalRequests


class TestItemInfo:

    def __init__(self, rp_requests: ReportPortalRequests, url_parts: UrlParts, item_type: str = "TEST"):
        self.rp_request = rp_requests
        self.url_parts = url_parts.test_item
        self.item_type = item_type.upper()

    def get_info(self, uuid: str, cache: bool = True, ttl: int = None):
        return self.rp_request.get_info(
            url_parts=self.url_parts,
            uuid=uuid,
            cache=cache,
            ttl=ttl
        )

    def get_id(self, uuid: str, cache: bool = True, ttl: int = None):
        return self.rp_request.get_id(
            url_parts=self.url_parts,
            uuid=uuid,
            cache=cache,
            ttl=ttl
        )

    def get_items(self, **kwargs: any) -> list[dict]:
        return self.rp_request.get_items(url_parts=self.url_parts, **kwargs)
