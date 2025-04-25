# -*- coding: utf-8 -*-
from .client import Client
from .launcher import Launcher

from .suite import Suite
from .test import Test
from .test_item import TestItem


class ReportPortal:

    def __init__(self, project_name: str, config_path: str = None):
        self.project_name = project_name
        self.client = Client(config_path=config_path)
        self.__launcher = Launcher(project_name=project_name, client=self.client)

    @property
    def launch(self):
        return self.__launcher

    def create_test(self, name: str):
        return Test(self.__launcher, name=name)

    def suite(self):
        return Suite(self.__launcher)

    def test_item(self, item_type: str = "TEST") -> TestItem:
        return TestItem(self.__launcher, item_type=item_type)
