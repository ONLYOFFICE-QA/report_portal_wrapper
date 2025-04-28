# -*- coding: utf-8 -*-
import time
from typing import Any
from .decorators import singleton


@singleton
class Cache:

    def __init__(self):
        self._store = {}

    def get(self, key: str) -> Any | None:
        entry = self._store.get(key)

        if entry is None:
            return None

        value, expire_time = entry
        if expire_time and time.time() > expire_time:
            del self._store[key]
            return None

        return value

    def set(self, key: str, value: any, ttl=None):
        expire_time = time.time() + ttl if ttl else None
        self._store[key] = (value, expire_time)

    def clear(self):
        self._store.clear()

    def delete(self, key):
        self._store.pop(key, None)