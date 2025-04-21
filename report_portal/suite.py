# -*- coding: utf-8 -*-
from typing import Optional, Dict, Any

from reportportal_client import RPClient
from reportportal_client.helpers import timestamp


class Suite:
    def __init__(self, client: RPClient):
        self.client = client
        self.item_id = None

    def start_suite(
            self,
            suite_name: str,
            item_type: str = "SUITE",
            attributes: Optional[Dict[str, Any]] = None,
            description: Optional[str] = None,
            parameters: Optional[dict] = None,
            parent_item_id: Optional[str] = None,
            has_stats: bool = True,
            code_ref: Optional[str] = None,
            retry: bool = False,
            test_case_id: Optional[str] = None,
            retry_of: Optional[str] = None,
            uuid: Optional[str] = None,
            **kwargs: Any
    ) -> str:
        try:
            item_id = self.client.start_test_item(
                name=suite_name,
                start_time=timestamp(),
                item_type=item_type,
                description=description,
                attributes=attributes,
                parameters=parameters,
                parent_item_id=parent_item_id,
                has_stats=has_stats,
                code_ref=code_ref,
                retry=retry,
                test_case_id=test_case_id,
                retry_of=retry_of,
                uuid=uuid,
                **kwargs
            )
            return self.item_id

        except Exception as e:
            raise RuntimeError(f"Failed to create: '{suite_name}': {e}")

    def finish_suite(self, suite_id: str = None):
        item_id = suite_id or self.item_id
        self.client.finish_test_item(item_id=item_id, end_time=timestamp())

    def create(self, suite_name: str, parent_suite_id: str = None) -> str:
        suite_id = self.start_suite(suite_name, parent_item_id=parent_suite_id)
        self.finish_suite(suite_id)
        return suite_id
