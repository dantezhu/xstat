# -*- coding: utf-8 -*-

from statsd import StatsClient

from utils import catch_exc
import constants


class DjangoStat(object):
    _stat_title = None
    _stat_host = None
    _stat_port = None

    _stat_client = None

    def __init__(self):
        from django.conf import settings

        super(DjangoStat, self).__init__()

        self._stat_title = getattr(settings, 'STAT_TITLE', None)
        self._stat_host = getattr(settings, 'STAT_HOST', None)
        self._stat_port = getattr(settings, 'STAT_PORT', None) or constants.STAT_PORT

        self._stat_client = StatsClient(host=self._stat_host, port=self._stat_port)

    @catch_exc
    def process_request(self, request):
        request.stat_timers = []
        request.stat_timers.append(
            self._stat_client.timer('.'.join([
                self._stat_title,
                'endpoint',
                request.resolver_match.url_name,
                ])
            )
        )

        request.stat_timers.append(
            self._stat_client.timer('.'.join([
                self._stat_title,
                'all',
                ])
            )
        )

        for stat in request.stat_timers:
            stat.start()

    @catch_exc
    def process_response(self, request, response):
        """
        无论是否抛出异常，都会执行这一步
        """
        if not hasattr(request, 'stat_timers'):
            return response

        for stat in request.stat_timers:
            stat.stop()

        return response
