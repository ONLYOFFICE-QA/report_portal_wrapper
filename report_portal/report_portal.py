# -*- coding: utf-8 -*-
from .client import Client
from .launch import Launch

from .suite import Suite
from .test import Test


class ReportPortal:

    def __init__(self, project_name: str, config_path: str = None):
        self.project_name = project_name
        self.client = Client(config_path).create(project_name)

    @property
    def launcher(self):
        return Launch(self.client)

    @property
    def test(self):
        return Test(self.client)

    @property
    def suite(self):
        return Suite(self.client)
