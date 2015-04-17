# -*- coding: utf-8 -*-

from statsd import StatsClient

from utils import catch_exc
import constants


class FlaskStat(object):

    _xstat_title = None
    _xstat_host = None
    _xstat_port = None

    _stat_client = None

    def __init__(self, app=None):
        super(FlaskStat, self).__init__()

        if app:
            self.init_app(app)

    def init_app(self, app):
        from flask import request, g
        """
        绑定app
        """
        self._xstat_title = app.config.get('XSTAT_TITLE')
        self._xstat_host = app.config.get('XSTAT_HOST')
        self._xstat_port = app.config.get('XSTAT_PORT') or constants.XSTAT_PORT
        self._stat_client = StatsClient(host=self._xstat_host, port=self._xstat_port)

        @app.before_request
        @catch_exc
        def prepare_stat():
            if not request.endpoint:
                return

            g.xstat_timers = []
            g.xstat_timers.append(
                self._stat_client.timer('.'.join([
                    self._xstat_title,
                    'endpoint',
                    request.endpoint,
                    ])
                )
            )

            g.xstat_timers.append(
                self._stat_client.timer('.'.join([
                    self._xstat_title,
                    'all',
                    ])
                )
            )

            for stat in g.xstat_timers:
                stat.start()

        @app.teardown_request
        @catch_exc
        def send_stat(exc):
            if not hasattr(g, 'xstat_timers'):
                return

            for stat in g.xstat_timers:
                stat.stop()
