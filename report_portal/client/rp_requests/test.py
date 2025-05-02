# -*- coding: utf-8 -*-
from .test_item import TestItem


class Test(TestItem):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, item_type="TEST", **kwargs)

    def get_tests(
            self,
            launch_id: str,
            page_size: int = 100,
            cache: bool = False,
            ttl: int = None
    ) -> list[dict]:
        return self.get_items_by_type(launch_id=launch_id, page_size=page_size, cache=cache, ttl=ttl)


    def get_tests_by_name(
            self,
            launch_id: str,
            name: str,
            page_size: int = 100,
            cache: bool = False,
            ttl: int = None
    ) -> list[dict]:
        return self.get_items(launch_id=launch_id, filter_by_name=name, page_size=page_size, cache=cache, ttl=ttl)

