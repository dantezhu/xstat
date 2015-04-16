# -*- coding: utf-8 -*-

import time
from flask import Flask
from webstat import FlaskStat

DEBUG = True

STAT_TITLE = 'dante.test'
STAT_HOST = '42.96.128.64'
STAT_FORBID_PATHS = [r'^/forbid']
STAT_ALLOW_PATHS = [r'^/allow', r'/forbid']
STAT_HACK_PATHS = [
    (r'/all(\S+)', r'/\g<1>/ok'),
]

app = Flask(__name__)
app.config.from_object(__name__)

fga = FlaskStat(app)


@app.route('/allow')
def allow():
    time.sleep(1)
    return u'ok'


@app.route('/forbid')
def forbid():
    time.sleep(1)
    return u'forbid'

if __name__ == '__main__':
    app.run()
