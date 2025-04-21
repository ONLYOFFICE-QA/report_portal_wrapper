# -*- coding: utf-8 -*-
from .client import Client
from .report_portal_launcher import ReportPortalLauncher
from .report_portal_test import ReportPortalTest
from .suite import Suite


class ReportPortal:

    def __init__(self, project_name: str, config_path: str = None):
        self.project_name = project_name
        self.client = Client(config_path).create(project_name)

    @property
    def launcher(self):
        return ReportPortalLauncher(self.client)

    @property
    def test(self):
        return ReportPortalTest(self.client)

    @property
    def suite(self):
        return Suite(self.client)
