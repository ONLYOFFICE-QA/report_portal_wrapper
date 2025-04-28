# -*- coding: utf-8 -*-
from report_portal.client import ReportPortalRequests
from report_portal.info.launch import LaunchInfo
from report_portal.info.suite import SuiteInfo
from report_portal.info.test import TestInfo
from report_portal.info.test_item import TestItemInfo
from report_portal.info.url_parts import UrlParts


class Info:

    def __init__(self, rp_requests: ReportPortalRequests, project_name: str):
        self.requests = rp_requests
        self.url_parts = UrlParts(project_name=project_name)
        self.suite = SuiteInfo(rp_requests=self.requests, url_parts=self.url_parts)
        self.launch = LaunchInfo(rp_requests=self.requests, url_parts=self.url_parts)
        self.test = TestInfo(rp_requests=self.requests, url_parts=self.url_parts)
        self.test_item = TestItemInfo(rp_requests=self.requests, url_parts=self.url_parts)
