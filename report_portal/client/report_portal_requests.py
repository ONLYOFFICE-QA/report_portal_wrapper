# -*- coding: utf-8 -*-
import requests

class ReportPortalRequests:

    def __init__(self, config: dict, api_version: str = "v1"):
        self.api_version = api_version
        self.config = config
        self.__api_key = config["api_key"]
        self.__endpoint = config["endpoint"]
        self.headers = self._get_headers()

    def get(self, url_parts: str, params: dict = None) -> dict | None:
        headers = {
            "Authorization": f"Bearer {self.__api_key}"
        }

        _url = f"{self._get_base_url()}/{url_parts}"

        response = requests.get(_url, headers=headers, params=params or {})

        if response.status_code == 200:
            return response.json()

        print(f"|ERROR| Response to {_url} failed\nStatus code: {response.status_code}\nError: {response.text}")
        return None

    def _get_base_url(self) -> str:
        return f"{self.__endpoint}/api/{self.api_version}"

    def _get_headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.__api_key}"
        }
