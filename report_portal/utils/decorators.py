# -*- coding: utf-8 -*-
from functools import wraps



def cacheable(default_ttl: int = None):
    from .cache import Cache

    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if not hasattr(self, '__method_cache'):
                self.__method_cache = Cache()

            cache_kwargs = kwargs.copy()

            use_cache = cache_kwargs.pop('cache', True)
            ttl = cache_kwargs.pop('ttl', default_ttl)

            if not use_cache:
                return func(self, *args, **kwargs)

            cache_key = f"{func.__name__}:{args}:{str(cache_kwargs)}"

            cached = self.__method_cache.get(cache_key)
            if cached is not None:
                return cached

            result = func(self, *args, **kwargs)
            if result is not None:
                self.__method_cache.set(cache_key, result, ttl=ttl)
            return result

        return wrapper
    return decorator


def singleton(class_):
    __instances = {}

    @wraps(class_)
    def getinstance(*args, **kwargs):
        if class_ not in __instances:
            __instances[class_] = class_(*args, **kwargs)
        return __instances[class_]

    return getinstance




