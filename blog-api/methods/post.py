import logging

from sanic import Blueprint
from sanic.request import Request
from sanic.response import HTTPResponse


bp = Blueprint('blog_posts')


@bp.get('/post/<id:int>')
def get_post(request: Request) -> HTTPResponse:
    services = request.app.services
    post_storage = services.post_storage
    body = request.json

    id = body.get('id')

    # For current testing/debugging purposes:
    logging.info('blog id TEST ---->', id)

    return HTTPResponse(status=200)


