# -*- coding: utf-8 -*-

"""
配置项:
    * STAT_TITLE : 统计的顶级目录，可以为 x.y，这样就是两层目录
    * STAT_HOST : statsd服务器IP
    STAT_PORT : statsd服务器端口
    STAT_FORBID_PATHS : 被拒绝的paths，优先级高于 STAT_ALLOW_PATHS
    STAT_ALLOW_PATHS : 被允许的paths
    STAT_HACK_PATHS: 上报时按照规则替换，在allow和forbid判断之后进行. 示例: [(r'^/all(\S+)', r'ok\g<1>')]
"""

__version__ = '0.1.5'

from .django_stat import DjangoStat
from .flask_stat import FlaskStat
