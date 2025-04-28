from typing import Optional, Tuple, Union

from .launcher import Launcher
from .test_item import TestItem


class Test(TestItem):

    def __init__(self, launcher: Launcher):
        super().__init__(launcher=launcher, item_type="TEST")

    def get_tests(self) -> list[dict]:
        return self.get_items_by_type()
