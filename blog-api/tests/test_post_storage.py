from services.post_storage import PostStorage


def test_get_post():
    post_storage = PostStorage()

    # Using existing demo logic in PostStorage to seed the testdb; for non-demo purposes, will move
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

# TODO: add tests for create comment, create post (then test linking comments to posts)

