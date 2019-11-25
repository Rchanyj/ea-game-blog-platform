import time

from services.post_storage import PostStorage


def test_get_post():
    post_storage = PostStorage()

    # Using existing demo logic in PostStorage to seed the testdb; for post-MVP, will move
    # demo seed logic into tests.
    post_storage.init()

    post_id = 100001
    post_data = post_storage.get_post(post_id)

    assert (len(post_data), post_data[0]) == (5, 100001)


def test_get_posts():
    post_storage = PostStorage()
    post_storage.init()

    limit = 10
    offset = 40

    expected_post_id = 100000

    posts_data = post_storage.get_posts(limit, offset)

    assert (len(posts_data), posts_data[9][0]) == (10, expected_post_id)


def test_get_comments():
    post_storage = PostStorage()
    post_storage.init()

    post_id = 100000

    comments_data = post_storage.get_comments(post_id)

    assert len(comments_data) == 3


def test_save_post():
    post_storage = PostStorage()
    post_storage.init()

    post_content = {
        'id': 123456,
        'author': 'noobmaster64',
        'title': 'SW: Fallen Order is Awesome',
        'text': 'This game is awesome yeet',
        'created_time': time.time()
    }

    post_storage.save_post(post_content)

    saved_post = post_storage.get_post(123456)

    assert saved_post == (post_content.get('id'),
                          post_content.get('author'),
                          post_content.get('title'),
                          post_content.get('text'),
                          post_content.get('created_time'))


def test_save_comment():
    post_storage = PostStorage()
    post_storage.init()

    comment_content = {
        'id': 12345,
        'post_id': 123456,
        'author': 'masternoob46',
        'text': 'Totally not commenting on my own post with an alt name...',
        'created_time': time.time()
    }

    post_storage.save_comment(comment_content)
    post_id = 123456

    saved_comment = post_storage.get_comments(post_id)

    assert saved_comment[0] == (comment_content.get('id'),
                                comment_content.get('post_id'),
                                comment_content.get('author'),
                                comment_content.get('text'),
                                comment_content.get('created_time'))

# Future wish list: exception handling testing...
