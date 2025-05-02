# -*- coding: utf-8 -*-
from .launcher import Launcher
from .test_item import TestItem


class Test(TestItem):

    def __init__(self, launcher: Launcher):
        super().__init__(launcher=launcher, item_type="TEST")
        self.request = launcher.client.rp_request.test
