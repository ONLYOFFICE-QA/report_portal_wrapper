# -*- coding: utf-8 -*-
from ..client import ReportPortalRequests
from .launch import LaunchInfo
from .suite import SuiteInfo
from .test import TestInfo
from .test_item import TestItemInfo
from .url_parts import UrlParts


class Info:

    def __init__(self, rp_requests: ReportPortalRequests, project_name: str):
        self.requests = rp_requests
        self.url_parts = UrlParts(project_name=project_name)
        self.suite = SuiteInfo(rp_requests=self.requests, url_parts=self.url_parts)
        self.launch = LaunchInfo(rp_requests=self.requests, url_parts=self.url_parts)
        self.test = TestInfo(rp_requests=self.requests, url_parts=self.url_parts)
        self.test_item = TestItemInfo(rp_requests=self.requests, url_parts=self.url_parts)
