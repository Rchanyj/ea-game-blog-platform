import logging

from sanic import Blueprint
from sanic.request import Request
from sanic.response import HTTPResponse


bp = Blueprint('blog_posts')


@bp.get('/post/<id:int>')
def get_post(request: Request, id: int) -> HTTPResponse:
    services = request.app.services
    post_storage = services.post_storage
    body = request.json

    # For current testing/debugging purposes:
    # print('blog id TEST ---->', id)
    # post_content = post_storage.get_post(id)
    # logging.info('should return nothing ---->', post_content)
    # print('should return nothing ---->', post_content)

    return HTTPResponse(status=200)
