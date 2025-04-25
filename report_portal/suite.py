# -*- coding: utf-8 -*-
from report_portal.launcher import Launcher
from report_portal.test_item import TestItem


class Suite:

    def __init__(self, launcher: Launcher):
        self.launcher = launcher
        self.test_item = TestItem(launcher=self.launcher, item_type="SUITE")

    @property
    def uuid(self):
        if not self.test_item.item_uuid:
            raise RuntimeError("Suite item has not been started. Cannot finish the suite.")
        return self.test_item.item_uuid

    def start(self, suite_name: str, parent_suite_uuid: str, **kwargs) -> str:
        return self.test_item.start(name=suite_name, parent_item_id=parent_suite_uuid, **kwargs)

    def finish(self, return_code: int, suite_uuid: str = None, **kwargs):
        self.test_item.finish(return_code=return_code, item_id=suite_uuid, **kwargs)

    def create(self, suite_name: str, parent_suite_id: str = None, **kwargs) -> str:
        suite_uuid = self.start(suite_name=suite_name, parent_suite_uuid=parent_suite_id, **kwargs)
        self.finish(return_code=0, suite_uuid=suite_uuid, **kwargs)
        return suite_uuid

    def get_info(self, uuid: str = None):
        return self.test_item.get_info(uuid=uuid)

    def get_id(self, uuid: str = None):
        return self.get_info(uuid=uuid).get("id")

    def get_suites(self) -> list[dict]:
        return self.test_item.get_items_by_type()

