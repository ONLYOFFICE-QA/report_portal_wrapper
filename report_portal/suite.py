# -*- coding: utf-8 -*-
from report_portal.launcher import Launcher
from report_portal.test_item import TestItem


class Suite(TestItem):

    def __init__(self, launcher: Launcher):
        super().__init__(launcher=launcher, item_type="SUITE")
        self.info = launcher.info_client.suite


    def create(self, suite_name: str, parent_suite_id: str = None, **kwargs) -> str:
        suite_uuid = self.start(suite_name=suite_name, parent_suite_uuid=parent_suite_id, **kwargs)
        self.finish(return_code=0, suite_uuid=suite_uuid, **kwargs)
        return suite_uuid
