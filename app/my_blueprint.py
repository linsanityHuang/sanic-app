from sanic.response import json
from sanic import Blueprint

bp = Blueprint('my_blueprint', url_prefix='bp1')


@bp.route('/')
async def bp_root(request):
    return json({'my': 'blueprint'})
