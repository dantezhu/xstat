# -*- coding: utf-8 -*-

import re
from log import logger


class StatAdapter(object):
    _stat_title = None
    _stat_host = None
    _stat_port = None
    _stat_forbid_paths = None
    _stat_allow_paths = None
    _stat_hack_paths = None

    _stat_client = None

    def should_stat(self, path):
        """
        request是否要被统计
        """

        # 先判断是否在forbid列表里，只要发现就直接拒绝
        if filter(lambda x: re.match(x, path), self._stat_forbid_paths or tuple()):
            logger.debug('path is in forbid paths. path: %s', path)
            return False

        # 改成不为None就有效，这样空列表也是生效的
        if self._stat_allow_paths is not None:
            if not filter(lambda x: re.match(x, path), self._stat_allow_paths):
                logger.debug('path is not in allow paths. path: %s', path)
                return False

        return True

    def hack_path(self, path):
        """
        将path替换为需要上报的
        """
        if not self._stat_hack_paths:
            return path

        for src_p, dst_p in self._stat_hack_paths:
            if not re.match(src_p, path):
                continue

            try:
                return re.sub(src_p, dst_p, path)
            except Exception, e:
                logger.error('re.sub fail. path: %s, src_p:%s, dst_p: %s, e: %s', path, src_p, dst_p, e)
                return path

        return path

    def replace_dot(self, src, to='_'):
        return (src or '').replace('.', to)