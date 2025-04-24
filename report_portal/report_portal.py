# -*- coding: utf-8 -*-
from .client import Client
from .launcher import Launcher

from .suite import Suite
from .test import Test


class ReportPortal:

    def __init__(self, project_name: str, config_path: str = None):
        self.project_name = project_name
        self.client = Client(config_path=config_path)
        self.__launcher = Launcher(project_name=project_name, client=self.client)

    @property
    def launch(self):
        return self.__launcher

    @property
    def test(self):
        return Test(self.__launcher)

    @property
    def suite(self):
        return Suite(self.__launcher)
