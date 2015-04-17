# -*- coding: utf-8 -*-

from statsd import StatsClient

from utils import catch_exc
import constants


class MapleStat(object):

    _xstat_title = None
    _xstat_host = None
    _xstat_port = None

    _stat_client = None

    def __init__(self, app=None, config=None):
        super(MapleStat, self).__init__()

        if app:
            self.init_app(app, config)

    def init_app(self, app, config):
        """
        绑定app
        """
        self._xstat_title = config.get('XSTAT_TITLE')
        self._xstat_host = config.get('XSTAT_HOST')
        self._xstat_port = config.get('XSTAT_PORT') or constants.XSTAT_PORT
        self._stat_client = StatsClient(host=self._xstat_host, port=self._xstat_port)

        @app.before_request
        @catch_exc
        def prepare_stat(request):
            if not request.endpoint:
                return

            request.xstat_timers = []
            request.xstat_timers.append(
                self._stat_client.timer('.'.join([
                    self._xstat_title,
                    'endpoint',
                    request.endpoint,
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

        @app.after_request
        @catch_exc
        def send_stat(request, exc):
            if not hasattr(request, 'xstat_timers'):
                return

            for stat in request.xstat_timers:
                stat.stop()
