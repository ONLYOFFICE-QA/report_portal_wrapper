# -*- coding: utf-8 -*-
import time
import requests

from .config import Config
from ..utils import singleton, cacheable


@singleton
class ReportPortalRequests:

    def __init__(self, config: Config):
        self.session = requests.Session()
        self.config = config
        self.__api_key = config.api_key
        self.__endpoint = config.endpoint
        self.api_version = self._validate_api_version(version=self.config.api_version or "v1")
        self.headers = self._get_headers()
        self.base_url = self._get_base_url()

    @cacheable()
    def get(
            self,
            url_parts: str,
            params: dict = None,
            max_retries: int = 3,
            interval: float = 0.5,
            cache: bool = False,
            ttl: int = None
    ) -> dict | None:
        f"""|INFO| Parameters {cache} and {ttl} for cacheable decorator"""

        _url = f"{self.base_url}/{url_parts}"

        for attempt in range(max_retries):
            response = self.session.request(method="GET", url=_url, params=params or {}, headers=self.headers)

            if response.status_code == 200:
                return response.json()
            else:
                print(
                    f"|ERROR| Attempt {attempt + 1} failed for {_url}\n"
                    f"Status code: {response.status_code}\nError: {response.text}"
                )

                if attempt < max_retries - 1:
                    time.sleep(interval)

        return None

    @cacheable()
    def get_info(self, url_parts: str, uuid: str, cache: bool = True, ttl: int = None) -> dict | None:
        return self.get(f"{url_parts}/uuid/{uuid}", cache=cache, ttl=ttl)

    def get_id(self, url_parts: str, uuid: str, cache: bool = True, ttl: int = None) -> str | None:
        info = self.get_info(url_parts=url_parts, uuid=uuid, cache=cache, ttl=ttl)
        return info.get('id') if info else None

    def get_items(
            self,
            url_parts: str,
            filter_by_name: str = None,
            filter_by_status: str = None,
            filter_by_launch_id: str = None,
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
            "filter.eq.launchId": filter_by_launch_id,
            "filter.eq.type": filter_by_type.upper() if filter_by_type else None,
            "sort": sort
        }

        _params.update({key: value for key, value in filters.items() if value is not None})

        while True:
            _params["page.page"] = page
            data = self.get(url_parts, params=_params, max_retries=max_retries, interval=interval, cache=cache, ttl=ttl)
            page_content = data.get("content", [])
            items.extend(page_content)

            if page > data.get("page", {}).get("totalPages", 1):
                break

            page += 1

        return items

    def _get_base_url(self) -> str:
        return f"{self.__endpoint}/api/{self.api_version}"

    def _get_headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.__api_key}"
        }

    @staticmethod
    def _validate_api_version(version: str) -> str:
        _api_version = version.lower()
        if _api_version not in ["v1", "v2"]:
            raise ValueError(f"Invalid API version: {_api_version}. Must be one of ['v1', 'v2'].")

        return _api_version
