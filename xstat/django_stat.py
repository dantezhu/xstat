# -*- coding: utf-8 -*-

from statsd import StatsClient

from utils import catch_exc
import constants


class DjangoStat(object):
    _xstat_title = None
    _xstat_host = None
    _xstat_port = None

    _stat_client = None

    def __init__(self):
        from django.conf import settings

        super(DjangoStat, self).__init__()

        self._xstat_title = getattr(settings, 'XSTAT_TITLE', None)
        self._xstat_host = getattr(settings, 'XSTAT_HOST', None)
        self._xstat_port = getattr(settings, 'XSTAT_PORT', None) or constants.XSTAT_PORT

        self._stat_client = StatsClient(host=self._xstat_host, port=self._xstat_port)

    @catch_exc
    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        request.resolver_match.url_name 在process_view才可以取到
        :return:
        """
        request.xstat_timers = []
        request.xstat_timers.append(
            self._stat_client.timer('.'.join([
                self._xstat_title,
                'endpoint',
                request.resolver_match.url_name,
                ])
            )
        )

        request.xstat_timers.append(
            self._stat_client.timer('.'.join([
                self._xstat_title,
                'all',
                ])
            )
        )

        for stat in request.xstat_timers:
            stat.start()

    @catch_exc
    def process_response(self, request, response):
        """
        无论是否抛出异常，都会执行这一步
        """
        if not hasattr(request, 'xstat_timers'):
            return response

        for stat in request.xstat_timers:
            stat.stop()

        return response
