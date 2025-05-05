# -*- coding: utf-8 -*-
import time
import requests

from typing import Optional

from ..config import Config
from ...utils import singleton, cacheable


@singleton
class ReportPortalRequests:

    def __init__(self, config: Config, session: Optional[requests.Session] = None):
        self.session = session or requests.Session()
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

    def post(
            self,
            url_parts: str,
            data: dict,
    ) -> dict | None:
        _url = f"{self.base_url}/{url_parts}"
        response = self.session.request(method="POST", url=_url, json=data, headers=self.headers)
        if response.status_code == 200 or response.status_code == 201:
            return response.json()
        else:
            print(f"|ERROR| Post request failed for {_url}\nError: {response.text}\nStatus code: {response.status_code}")
            return None

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

    def uri_join(*uri_parts: str) -> str:
        """Join uri parts.

        Avoiding usage of urlparse.urljoin and os.path.join
        as it does not clearly join parts.
        Args:
            *uri_parts: tuple of values for join, can contain back and forward
                        slashes (will be stripped up).
        Returns:
            An uri string.
        """
        return "/".join(str(s).strip("/").strip("\\") for s in uri_parts)
