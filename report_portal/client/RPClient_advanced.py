# -*- coding: utf-8 -*-
from typing import Optional, Union, Any

from reportportal_client import RPClient
from reportportal_client.core.rp_requests import HttpRequest
from reportportal_client.helpers import verify_value_length, uri_join, timestamp

from .rp_requests import UrlParts
from .rp_requests.report_portal_requests import ReportPortalRequests


class RPClientAdvanced(RPClient):

    def __init__(self,
        endpoint: str,
        project: str,
        api_key: str = None,
        launch_uuid: str | None = None,
        **kwargs
    ):
        super().__init__(
            endpoint=endpoint,
            project=project,
            api_key=api_key,
            launch_uuid=launch_uuid,
            **kwargs
        )
        self.requests = ReportPortalRequests()
        self.url_parts = UrlParts(project_name=self.project)

    def update_test_item(
        self,
        item_uuid: str,
        attributes: Optional[Union[list, dict]] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
        **kwargs: Any
    ) -> Optional[str]:
        """Update existing Test Item at the ReportPortal.

        :param status: Test Item status.
        :param item_uuid:   Test Item UUID returned on the item start.
        :param attributes:  Test Item attributes: [{'key': 'k_name', 'value': 'k_value'}, ...].
        :param description: Test Item description.
        :return:            Response message or None.
        """
        data = {}

        _params = {
            "description": description,
            "attributes": verify_value_length(attributes) if self.truncate_attributes else attributes,
            "status": status,
            **kwargs
        }

        data.update({key: value for key, value in _params.items() if value is not None})

        item_id = self.get_item_id_by_uuid(item_uuid=item_uuid)

        url = uri_join(self.base_url_v1, "item", item_id, "update")
        response = HttpRequest(
            self.session.put,
            url=url,
            json=data,
            verify_ssl=self.verify_ssl,
            http_timeout=self.http_timeout,
            name="update_test_item",
        ).make()
        if not response:
            return None

        return response.message

    def send_log(
            self,
            launch_uuid: str,
            message: str,
            level: str = "INFO",
            item_uuid: str = None,
            time: str = None,
    ):
        return self.requests.log(
            url_parts=self.url_parts.log,
            launch_uuid=launch_uuid,
            message=message,
            log_time=time or timestamp(),
            item_uuid=item_uuid,
            level=level
        )

    def get_item_id_by_uuid(self, item_uuid: str) -> Optional[str]:
        """Get Test Item ID by the given Item UUID.

        :param item_uuid: String UUID returned on the Item start.
        :return:          Test Item ID.
        """
        return self.requests.get_id(url_parts=self.url_parts.test_item, uuid=item_uuid, cache=True, ttl=None)
