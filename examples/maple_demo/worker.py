# -*- coding: utf-8 -*-

from maple import Worker
from netkit.box import Box
from xstat import MapleStat
import user

app = Worker(Box)
app.register_blueprint(user.bp)

maple_stat = MapleStat(app, dict(
    XSTAT_TITLE='dante.test',
    XSTAT_HOST='127.0.0.1',
))


@app.route(1)
def register(request):
    request.write_to_client(dict(
        ret=0
    ))

if __name__ == '__main__':
    app.run('127.0.0.1', 28000, debug=True)
