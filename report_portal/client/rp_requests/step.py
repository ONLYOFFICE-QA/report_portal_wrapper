# -*- coding: utf-8 -*-
from .test_item import TestItem


class Step(TestItem):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, item_type="STEP", **kwargs)

    def get_steps_by_name(
            self,
            launch_id: str,
            name: str,
            page_size: int = 100,
            cache: bool = False,
            ttl: int = None
    ) -> list[dict]:
        return self.get_items(launch_id=launch_id, filter_by_name=name, page_size=page_size, cache=cache, ttl=ttl)
