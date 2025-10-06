# -*- coding: utf-8 -*-
from .launcher import Launcher
from .test_item import TestItem


class Step(TestItem):
    """Represents a step item in ReportPortal."""

    def __init__(self,  launcher: Launcher):
        super().__init__(launcher=launcher, item_type="STEP")
