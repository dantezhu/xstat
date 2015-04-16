# -*- coding: utf-8 -*-

from statsd import StatsClient

from stat_adapter import StatAdapter
from utils import catch_exc


class DjangoStat(StatAdapter):

    def __init__(self):
        from django.conf import settings

        super(DjangoStat, self).__init__()

        self._stat_title = getattr(settings, 'STAT_TITLE', None)
        self._stat_host = getattr(settings, 'STAT_HOST', None)
        self._stat_port = getattr(settings, 'STAT_PORT', None)
        self._stat_forbid_paths = getattr(settings, 'STAT_FORBID_PATHS', None)
        self._stat_allow_paths = getattr(settings, 'STAT_ALLOW_PATHS', None)
        self._stat_hack_paths = getattr(settings, 'STAT_HACK_PATHS', None)

        self._stat_client = StatsClient(host=self._stat_host, port=self._stat_port)

    @catch_exc
    def process_request(self, request):
        if not self.should_stat(request.path):
            return

        stat_name = '.'.join([
            self.replace_dot(self._stat_title),
            self.replace_dot(request.path),
            ])

        request.stat_timer = self._stat_client.timer(stat_name)
        request.stat_timer.start()

    @catch_exc
    def process_response(self, request, response):
        """
        无论是否抛出异常，都会执行这一步
        """
        if not hasattr(request, 'stat_timer'):
            return response

        request.stat_timer.stop()

        return response
