# -*- coding: utf-8 -*-
from .launch import Launch
from .report_portal_requests import ReportPortalRequests
from .suite import Suite
from .test import Test
from .test_item import TestItem
from .url_parts import UrlParts
from ..config import Config
from .step import Step


class RpRequests:

    def __init__(self, config: Config, url_parts: UrlParts, launch_id: str = None):
        self.__url_parts = url_parts
        self.config = config
        self.requests = ReportPortalRequests(config=self.config)
        self.suite = Suite(rp_requests=self.requests, url_parts=self.__url_parts, launch_id=launch_id)
        self.launch = Launch(rp_requests=self.requests, url_parts=self.__url_parts)
        self.test = Test(rp_requests=self.requests, url_parts=self.__url_parts, launch_id=launch_id)
        self.step = Step(rp_requests=self.requests, url_parts=self.__url_parts, launch_id=launch_id)
        self.test_item = TestItem(rp_requests=self.requests, url_parts=self.__url_parts, launch_id=launch_id)
