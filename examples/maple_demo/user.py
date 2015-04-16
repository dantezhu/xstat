# -*- coding: utf-8 -*-

from maple import Blueprint

bp = Blueprint('user')


@bp.route(100)
def get_info(request):
    request.write_to_client(dict(
        ret=0
    ))