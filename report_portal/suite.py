# -*- coding: utf-8 -*-
from report_portal.launcher import Launcher
from report_portal.test_item import TestItem


class Suite(TestItem):

    def __init__(self, launcher: Launcher):
        super().__init__(launcher=launcher, item_type="SUITE")

    def create(self, name: str, parent_item_id: str = None, return_code: int = 0, **kwargs) -> str:
        suite_uuid = self.start(name=name, parent_item_id=parent_item_id, **kwargs)
        self.finish(return_code=return_code, suite_uuid=suite_uuid, **kwargs)
        return suite_uuid
