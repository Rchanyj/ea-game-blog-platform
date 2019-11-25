import logging

from sanic import Blueprint
from sanic.request import Request
from sanic.response import HTTPResponse, json


bp = Blueprint('blog_posts')


@bp.get('/post/<id:int>')
def get_post(request: Request, id: int) -> HTTPResponse:
    services = request.app.services
    post_storage = services.post_storage

    post_data = post_storage.get_post(id)
    post_comments_data = post_storage.get_comments(id)
    post_comments = []

    for comment in post_comments_data:
        comment_content = {
            'id': comment[0],
            'author': comment[2],
            'text': comment[3],
            'created_time': comment[4]
        }
        post_comments.append(comment_content)

    post_content = {
        'id': post_data[0],
        'author': post_data[1],
        'title': post_data[2],
        'text': post_data[3],
        'created_time': post_data[4],
        'comments': post_comments
    }

    return json(post_content)
