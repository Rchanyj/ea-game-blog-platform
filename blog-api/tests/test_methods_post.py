import requests
import config

# (MVP) For simplicity, sticking with less code-intensive, direct url request testing;
# for future versions will use fixtures and set up test context


def test_get_post():
    host_url = 'http://localhost'
    post_id = 100000
    request_url = f'{host_url}:{config.LISTEN_PORT}/post/{post_id}'

    response = requests.get(request_url)
    actual_return = response.json()

    assert response.status_code == 200
    assert actual_return['id'] == post_id
    assert len(actual_return['comments']) == 3