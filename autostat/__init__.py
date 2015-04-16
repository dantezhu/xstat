# -*- coding: utf-8 -*-

"""
配置项:
    * STAT_TITLE : 统计的顶级目录，可以为 x.y，这样就是两层目录
    * STAT_HOST : statsd服务器IP
    STAT_PORT : statsd服务器端口
"""

__version__ = '0.1.6'

from .django_stat import DjangoStat
from .flask_stat import FlaskStat
from .maple_stat import MapleStat
