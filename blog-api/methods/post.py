import logging

from sanic import Blueprint
from sanic.request import Request
from sanic.response import HTTPResponse


bp = Blueprint('blog_posts')


@bp.get('/post/<id:int>')
def get_post(request: Request, id: int) -> HTTPResponse:
    services = request.app.services
    post_storage = services.post_storage

    # For current testing/debugging purposes:
    post_content = post_storage.get_post(id)
    print('should return post ---->', post_content)
    print('test post_content processing ----->', post_content[1])

    return HTTPResponse(status=200)
