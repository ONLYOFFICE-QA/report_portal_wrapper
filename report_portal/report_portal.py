# -*- coding: utf-8 -*-
from .client import Client
from .launcher import Launcher

from .suite import Suite
from .test import Test


class ReportPortal:

    def __init__(self, project_name: str, config_path: str = None):
        self.project_name = project_name
        self.client = Client(config_path).create(project_name)
        self.__launcher = Launcher(self.client)

    @property
    def launch(self):
        return self.__launcher

    @property
    def test(self):
        return Test(self.__launcher.get_client())

    @property
    def suite(self):
        return Suite(self.__launcher.get_client())
