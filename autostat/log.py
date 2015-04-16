# -*- coding: utf-8 -*-

import logging

logger = logging.getLogger('autostat')

import logging

LOG_FORMAT = '\n'.join((
    '/' + '-' * 80,
    '[%(levelname)s][%(asctime)s][%(process)d:%(thread)d][%(filename)s:%(lineno)d %(funcName)s]:',
    '%(message)s',
    '-' * 80 + '/',
))

logger = logging.getLogger('autostat')
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(LOG_FORMAT))
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
