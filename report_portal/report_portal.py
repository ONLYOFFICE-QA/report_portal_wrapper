# -*- coding: utf-8 -*-
from typing import Any

from .client import Client
from .info import Info
from .launcher import Launcher

from .suite import Suite
from .test import Test
from .test_item import TestItem


class ReportPortal:

    def __init__(self, project_name: str, config_path: str = None):
        self.project_name = project_name
        self.client = Client(config_path=config_path)
        self.info = Info(rp_requests=self.client.request, project_name=self.project_name)
        self.__launcher = Launcher(project_name=project_name, client=self.client, info=self.info)

    @property
    def launch(self) -> Launcher:
        return self.__launcher

    def get_launch_test(self) -> Test:
        return Test(launcher=self.__launcher)

    def get_launch_suite(self) -> Suite:
        return Suite(self.__launcher)

    def get_launch_test_item(self, item_type: str = "TEST") -> TestItem:
        return TestItem(self.__launcher, item_type=item_type)
