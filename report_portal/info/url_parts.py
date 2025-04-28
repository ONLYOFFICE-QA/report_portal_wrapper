# -*- coding: utf-8 -*-
from dataclasses import dataclass


@dataclass()
class UrlParts:
    project_name: str

    def __post_init__(self):
        self.test_item: str = f"{self.project_name}/item"
        self.launch: str = f"{self.project_name}/launch"
        self.test: str = f"{self.project_name}/test"
