# -*- coding: utf-8 -*-

from statsd import StatsClient

from utils import catch_exc
import constants


class FlaskStat(object):

    _stat_title = None
    _stat_host = None
    _stat_port = None

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
        self._stat_title = app.config.get('STAT_TITLE')
        self._stat_host = app.config.get('STAT_HOST')
        self._stat_port = app.config.get('STAT_PORT') or constants.STAT_PORT
        self._stat_client = StatsClient(host=self._stat_host, port=self._stat_port)

        @app.before_request
        @catch_exc
        def prepare_stat():
            g.stat_timers = []
            g.stat_timers.append(
                self._stat_client.timer('.'.join([
                    self._stat_title,
                    'endpoint',
                    request.endpoint,
                    ])
                )
            )

            g.stat_timers.append(
                self._stat_client.timer('.'.join([
                    self._stat_title,
                    'all',
                    ])
                )
            )

            for stat in g.stat_timers:
                stat.start()

        @app.teardown_request
        @catch_exc
        def send_stat(exc):
            if not hasattr(g, 'stat_timers'):
                return

            for stat in g.stat_timers:
                stat.stop()
