# -*- coding: utf-8 -*-

from statsd import StatsClient

from stat_adapter import StatAdapter
from utils import catch_exc


class FlaskStat(StatAdapter):

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
        self._stat_port = app.config.get('STAT_PORT') or 8125
        self._stat_forbid_paths = app.config.get('STAT_FORBID_PATHS')
        self._stat_allow_paths = app.config.get('STAT_ALLOW_PATHS')
        self._stat_hack_paths = app.config.get('STAT_HACK_PATHS')
        self._stat_client = StatsClient(host=self._stat_host, port=self._stat_port)

        @app.before_request
        @catch_exc
        def prepare_stat():
            if not self.should_stat(request.path):
                return

            stat_name = '.'.join([
                self._stat_title,
                self.replace_dot(request.path),
                ])

            g.stat_timer = self._stat_client.timer(stat_name)
            g.stat_timer.start()

        @app.teardown_request
        @catch_exc
        def send_stat(exc):
            if not hasattr(g, 'stat_timer'):
                return

            g.stat_timer.stop()
