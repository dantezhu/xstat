# -*- coding: utf-8 -*-

from statsd import StatsClient

import constants


class MapleStat(object):

    _stat_title = None
    _stat_host = None
    _stat_port = None

    _stat_client = None

    def __init__(self, app=None, config=None):
        super(MapleStat, self).__init__()

        if app:
            self.init_app(app, config)

    def init_app(self, app, config):
        """
        绑定app
        """
        self._stat_title = config.get('STAT_TITLE')
        self._stat_host = config.get('STAT_HOST')
        self._stat_port = config.get('STAT_PORT') or constants.STAT_PORT
        self._stat_client = StatsClient(host=self._stat_host, port=self._stat_port)

        @app.before_request
        def prepare_stat(request):
            request.stat_timers = []
            request.stat_timers.append(
                self._stat_client.timer('.'.join([
                    self._stat_title,
                    'endpoint',
                    request.endpoint,
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

        @app.after_request
        def send_stat(request, exc):
            if not hasattr(request, 'stat_timers'):
                return

            for stat in request.stat_timers:
                stat.stop()
