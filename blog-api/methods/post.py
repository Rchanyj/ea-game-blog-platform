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

    post_content = {}
    post_content.id = post_data[0]
    post_content.author = post_data[1]
    post_content.title = post_data[2]
    post_content.text = post_data[3]
    post_content.created_time = post_data[4]
    post_content.comments = []

    post_comments = post_storage.get_comments(id)

    for comment in post_comments:
        comment_content = {}
        comment_content.id = comment[0]
        comment_content.author = comment[2]
        comment_content.text = comment[3]
        comment_content.created_time = comment[4]

        post_content.comments.append(comment)

    return json(post_content)
