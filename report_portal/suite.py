# -*- coding: utf-8 -*-
from report_portal.launcher import Launcher
from report_portal.test_item import TestItem


class Suite:

    def __init__(self, launcher: Launcher):
        self.launcher = launcher
        self.test_item = TestItem(launcher=self.launcher, item_type="SUITE")

    def start(self, suite_name: str, **kwargs) -> str:
        return self.test_item.start(name=suite_name, **kwargs)

    def finish(self,*args, **kwargs):
        self.test_item.finish(*args, **kwargs)

    def create(self, suite_name: str, parent_suite_id: str = None) -> str:
        suite_id = self.start(suite_name, parent_item_id=parent_suite_id)
        self.finish(suite_id)
        return suite_id

    def get_suites(self):
        launch_id = self.launcher.id or self.launcher.get_launch_id_by_uuid()
        suites = []
        page = 1
        while True:
            params = {
                "filter.eq.type": "SUITE",
                "filter.eq.launchId": launch_id,
                "page.page": page,
                "page.size": 100
            }

            data = self.launcher.auth.request.get(self.test_item.url_parts, params=params)
            page_content = data.get("content", [])
            suites.extend(page_content)

            if data.get("page", {}).get("totalPages", 1) > page:
                page += 1
            else:
                break

        return suites

