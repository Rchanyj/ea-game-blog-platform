import requests
import config

# (MVP) For simplicity, sticking with less code-intensive, direct url request testing;
# for future versions will use fixtures and set up test context

host_url = 'http://localhost'


def test_get_post():
    post_id = 100000
    request_url = f'{host_url}:{config.LISTEN_PORT}/post/{post_id}'

    response = requests.get(request_url)
    actual_return = response.json()

    assert response.status_code == 200
    assert actual_return['id'] == post_id
    assert len(actual_return['comments']) == 3


def test_get_posts():
    request_url = f'{host_url}:{config.LISTEN_PORT}/posts'
    q = {
        'limit': 10,
        'offset': 0
    }

    response = requests.get(request_url, params=q)
    actual_return = response.json()

    assert response.status_code == 200
    assert len(actual_return) == 10


def test_create_post():
    request_url = f'{host_url}:{config.LISTEN_PORT}/create_post'

    content = {
        'author': 'noobmaster64',
        'title': 'I like mobas I cannot lie',
        'text': 'Ye'
    }

    response = requests.post(request_url, json=content)

    assert response.status_code == 200


def test_create_comment():
    request_url = f'{host_url}:{config.LISTEN_PORT}/create_comment'

    content = {
        'post_id': 1000000,
        'author': 'masternoob46',
        'text': 'poggers kappa omega'
    }

    response = requests.post(request_url, json=content)

    assert response.status_code == 200
