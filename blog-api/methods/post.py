import logging

from urllib import parse
from random import randint
import time

from sanic import Blueprint
from sanic.request import Request
from sanic.response import HTTPResponse, json


bp = Blueprint('blog_posts')


@bp.get('/post/<id:int>')
def get_post(request: Request, id: int) -> HTTPResponse:
    services = request.app.services
    post_storage = services.post_storage

    try:
        post_data = post_storage.get_post(id)
        post_comments_data = post_storage.get_comments(id)
    except Exception:
        logging.exception('Error fetching post data')
        raise Exception('Error fetching post data')

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


@bp.get('/posts')
def get_posts(request: Request) -> HTTPResponse:
    services = request.app.services
    post_storage = services.post_storage

    query_params = get_query_params(request.url)
    limit = query_params.get('limit', 20)
    offset = query_params.get('offset', 0)

    try:
        posts_content = post_storage.get_posts(limit, offset)
    except Exception:
        logging.exception('Error fetching posts')
        raise Exception('Error fetching posts')

    posts = []

    for post in posts_content:
        post_content = {
            'id': post[0],
            'author': post[1],
            'title': post[2],
            'text': post[3],
            'created_time': post[4]
        }
        posts.append(post_content)

    return json(posts)


@bp.post('/create_post')
def create_post(request: Request) -> HTTPResponse:
    services = request.app.services
    post_storage = services.post_storage

    post_content = request.json

    id = randint(1000000, 9999999)
    created_time = time.time()

    post_content['id'] = id
    post_content['created_time'] = created_time

    try:
        post_storage.save_post(post_content)
    except Exception:
        logging.exception('Failed to save post')
        raise Exception('Failed to save post')

    return HTTPResponse(status=200)


@bp.post('/create_comment')
def create_comment(request: Request) -> HTTPResponse:
    services = request.app.services
    post_storage = services.post_storage

    comment_content = request.json

    id = randint(100000, 999999)
    created_time = time.time()

    comment_content['id'] = id
    comment_content['created_time'] = created_time

    print(comment_content)

    try:
        post_storage.save_comment(comment_content)
    except Exception:
        logging.exception('Failed to save post')
        raise Exception('Failed to save post')

    return HTTPResponse(status=200)


def get_query_params(url):
    parsed_query = parse.parse_qs(parse.urlsplit(url).query)
    parsed = {
        'limit': int(parsed_query['limit'][0]),
        'offset': int(parsed_query['offset'][0])
    }
    return parsed
