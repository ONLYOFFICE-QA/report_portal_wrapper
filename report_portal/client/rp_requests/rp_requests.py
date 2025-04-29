# -*- coding: utf-8 -*-
from .launch import LaunchInfo
from .report_portal_requests import ReportPortalRequests
from .suite import SuiteInfo
from .test import TestInfo
from .test_item import TestItemInfo
from .url_parts import UrlParts
from ..config import Config


class RpRequests:

    def __init__(self, config: Config, url_parts: UrlParts):
        self.__url_parts = url_parts
        self.config = config
        self.requests = ReportPortalRequests(config=self.config)
        self.suite = SuiteInfo(rp_requests=self.requests, url_parts=self.__url_parts)
        self.launch = LaunchInfo(rp_requests=self.requests, url_parts=self.__url_parts)
        self.test = TestInfo(rp_requests=self.requests, url_parts=self.__url_parts)
        self.test_item = TestItemInfo(rp_requests=self.requests, url_parts=self.__url_parts)
