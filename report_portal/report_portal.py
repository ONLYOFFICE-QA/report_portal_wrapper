# -*- coding: utf-8 -*-
from .client import Client
from .launcher import Launcher
from .step import Step

from .suite import Suite
from .test import Test
from .test_item import TestItem


class ReportPortal:
    """
    Facade for interacting with ReportPortal entities.

    :param project_name: ReportPortal project name.
    :param config_path: Path to JSON config file; defaults to user config.
    """

    def __init__(self, project_name: str, config_path: str = None):
        self.project_name = project_name
        self.client = Client(config_path=config_path, project_name=self.project_name)
        self.__launcher = Launcher(client=self.client)

    @property
    def launch(self) -> Launcher:
        """
        Get the launch manager instance.

        :return: Launcher instance.
        """
        return self.__launcher

    def get_test(self) -> Test:
        """Get a Test helper instance for managing test items.

        Creates a Test helper bound to the current launcher that provides
        convenient methods for starting and finishing test cases.

        :return: Test instance bound to the current launcher.
        """
        return Test(self.__launcher)

    def get_suite(self) -> Suite:
        """Get a Suite helper instance for managing test suites.

        Creates a Suite helper bound to the current launcher that provides
        convenient methods for starting and finishing test suites.

        :return: Suite instance bound to the current launcher.
        """
        return Suite(self.__launcher)

    def get_step(self) -> Step:
        """Get a Step helper instance for managing test steps.

        Creates a Step helper bound to the current launcher that provides
        convenient methods for starting and finishing test steps.

        :return: Step instance bound to the current launcher.
        """
        return Step(self.__launcher)

    def get_test_item(self, item_type: str = "TEST") -> TestItem:
        """Create a TestItem helper for a specific item type.

        Provides a flexible way to create test item helpers for any supported
        ReportPortal item type (TEST, STEP, SUITE, etc.).

        :param item_type: Item type name like 'TEST', 'STEP', 'SUITE'.
        :return: New TestItem instance bound to the current launcher.
        """
        return TestItem(self.__launcher, item_type=item_type)

    # Deprecated aliases for backward compatibility
    def get_launch_test(self) -> Test:
        """Deprecated: Use get_test() instead."""
        return self.get_test()

    def get_launch_suite(self) -> Suite:
        """Deprecated: Use get_suite() instead."""
        return self.get_suite()

    def get_launch_step(self) -> Step:
        """Deprecated: Use get_step() instead."""
        return self.get_step()

    def get_launch_test_item(self, item_type: str = "TEST") -> TestItem:
        """Deprecated: Use get_test_item() instead.

        :param item_type: Item type name like 'TEST', 'STEP', 'SUITE'.
        """
        return self.get_test_item(item_type=item_type)
