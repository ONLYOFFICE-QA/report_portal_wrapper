# -*- coding: utf-8 -*-
from typing import Optional, Union, Any

from reportportal_client import RPClient
from reportportal_client.core.rp_requests import HttpRequest
from reportportal_client.helpers import verify_value_length

from .url_parts import UrlParts
from .rp_requests import ReportPortalRequests
from ..config import Config
from ...utils import cacheable


class RPClientAdvanced(RPClient):

    def __init__(self, config: Config, project_name: str, launch_uuid: str = None, **kwargs):
        self.config = config
        super().__init__(
            endpoint=self.config.endpoint,
            project=project_name,
            api_key=self.config.api_key,
            launch_uuid=launch_uuid,
            **kwargs
        )
        self.requests = ReportPortalRequests(config=self.config, session=self.session)
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

        url = self.requests.uri_join(self.base_url_v1, "item", item_id, "update")
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
            message: str,
            launch_uuid: str,
            time: str,
            item_uuid: str = None,
            level="INFO",
    ) -> Optional[dict]:
        base_data = {
            "launchUuid": launch_uuid,
            "time": time,
            "message": message,
            "level": level
        }

        addiction_param = {
            "itemUuid": item_uuid,
        }

        base_data.update({key: value for key, value in addiction_param.items() if value is not None})
        return self.requests.post(url_parts=self.url_parts.log, data=base_data)

    def get_item_id_by_uuid(self, item_uuid: str) -> Optional[str]:
        """Get Test Item ID by the given Item UUID.

        :param item_uuid: String UUID returned on the Item start.
        :return:          Test Item ID.
        """
        return self.get_id(item_type='test_item', uuid=item_uuid, cache=True, ttl=None)

    @cacheable()
    def get_info(self, item_type: str, uuid: str, cache: bool = True, ttl: int = None) -> dict | None:
        return self.requests.get(f"{self._get_url_parts(item_type)}/uuid/{uuid}", cache=cache, ttl=ttl)

    def get_id(self, item_type: str, uuid: str, cache: bool = True, ttl: int = None) -> str | None:
        info = self.get_info(item_type=item_type, uuid=uuid, cache=cache, ttl=ttl)
        return info.get('id') if info else None


    def get_items(
            self,
            item_type: str,
            launch_id: str = None,
            filter_by_name: str = None,
            filter_by_status: str = None,
            filter_by_type: str = None,
            page_size: int = 100,
            addition_params: dict = None,
            max_retries: int = 3,
            interval: float = 0.5,
            sort: str = None,
            cache: bool = False,
            ttl: int = None
    ) -> list[dict]:
        items = []
        page = 1

        _params = {
            "page.size": page_size,
            **(addition_params or {})
        }

        filters = {
            "filter.eq.name": filter_by_name,
            "filter.eq.status": filter_by_status.upper() if filter_by_status else None,
            "filter.eq.launchId": launch_id,
            "filter.eq.type": filter_by_type.upper() if filter_by_type else None,
            "sort": sort
        }

        _params.update({ key: value for key, value in filters.items() if value is not None })

        while True:
            _params["page.page"] = page
            data = self.requests.get(
                url_parts=self._get_url_parts(item_type),
                params=_params,
                max_retries=max_retries,
                interval=interval,
                cache=cache,
                ttl=ttl
            )

            if not data:
                break

            page_content = data.get("content", [])
            items.extend(page_content)

            if page > data.get("page", {}).get("totalPages", 1):
                break

            page += 1

        return items

    def _get_url_parts(self, item_type: str) -> str:
        _type = item_type.lower()
        if _type not in ["suite", "test", "step", "test_item", "launch"]:
            raise ValueError(f"Invalid item type: {_type}. Must be one of ['suite', 'test', 'step', 'test_item'].")

        if _type == "launch":
            url_parts = self.url_parts.launch
        else:
            url_parts = self.url_parts.test_item

        return url_parts
