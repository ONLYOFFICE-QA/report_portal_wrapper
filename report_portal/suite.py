# -*- coding: utf-8 -*-
from .launcher import Launcher
from .test_item import TestItem


class Suite(TestItem):
    """Represents a test suite entity in ReportPortal."""

    def __init__(self, launcher: Launcher):
        super().__init__(launcher=launcher, item_type="SUITE")

    def create(self, name: str, parent_item_id: str = None, return_code: int = 0, **kwargs) -> str:
        """Convenience method to start and immediately finish a suite.

        :param name: Suite name.
        :param parent_item_id: Optional parent item id.
        :param return_code: Return code to infer status.
        :return: Suite UUID.
        """
        suite_uuid = self.start(name=name, parent_item_id=parent_item_id, **kwargs)

        if not suite_uuid:
            raise RuntimeError(f"Can't create suite: name={name}, parent_item_id={parent_item_id}")

        self.finish(return_code=return_code, item_id=suite_uuid, **kwargs)
        return suite_uuid
