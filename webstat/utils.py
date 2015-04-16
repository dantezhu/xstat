# -*- coding: utf-8 -*-

from log import logger


def catch_exc(func):
    import functools

    @functools.wraps(func)
    def func_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            logger.error('exc occur.', exc_info=True)

    return func_wrapper
