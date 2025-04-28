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
    def launch(self) -> Launcher:
        return self.__launcher

    def create_test(self, name: str) -> Test:
        return Test(self.__launcher, name=name)

    @property
    def suite(self) -> Suite:
        return Suite(self.__launcher)

    def test_item(self, item_type: str = "TEST") -> TestItem:
        return TestItem(self.__launcher, item_type=item_type)

    def get_launches(self, filter_by_name: str = None, page_size: int = 100) -> list[dict]:
        return self.launch.get_launches(filter_by_name=filter_by_name, page_size=page_size)

    def get_items(
            self,
            name: str = None,
            item_type: str = None,
            filter_by_launch_id: bool = True,
            page_size: int = 100,
            cache: bool = False,
            ttl: int = None
    ) -> list[dict]:
        return self.client.request.get_items(
            url_parts=f"{self.project_name}/item",
            page_size=page_size,
            filter_by_name=name,
            filter_by_type=item_type,
            filter_by_launch_id=self.launch.id if filter_by_launch_id else None,
            cache=cache,
            ttl=ttl
        )
