from sanic import Blueprint
import sqlite3
from sqlite3 import Error

import logging


bp = Blueprint(__name__)


@bp.listener('before_server_start')
def attach(app, _):
    logging.info('Initializing post storage...')

    post_storage = PostStorage()
    post_storage.init()
    app.services.post_storage = post_storage


@bp.listener('after_server_stop')
def detach(app, _):
    logging.info('Closing post storage...')

    post_storage = app.services.post_storage
    if post_storage:
        post_storage.close()


# Create db tables:
create_posts_table = '''CREATE TABLE IF NOT EXISTS posts (
                            id integer PRIMARY KEY,
                            author text NOT NULL,
                            title text NOT NULL,
                            text text NOT NULL,
                            created_time timestamp NOT NULL
                        );'''

create_comments_table = '''CREATE TABLE IF NOT EXISTS comments (
                                id integer PRIMARY KEY,
                                post_id integer NOT NULL,
                                author text NOT NULL,
                                text text NOT NULL,
                                created_time timestamp NOT NULL,
                                FOREIGN KEY (post_id) REFERENCES posts (id)
                            );'''

# Queries:
sql_fetch_post = '''select *
                        from posts
                        where id = %s'''

sql_fetch_posts = '''select *
                        from posts
                        offset %s rows
                        fetch next %s rows only
                        order by created_time desc'''

sql_fetch_comments = '''select *
                            from comments
                            where post_id = %s
                            order by created_time desc'''


class PostStorage:

    def init(self):
        self.conn = None
        try:
            self.conn = sqlite3.connect(':memory:')
            cursor = self.conn.cursor()
            cursor.execute(create_posts_table)
            cursor.execute(create_comments_table)
        except Error:
            raise Exception('Failed to set up in-memory database.')

    def get_post(self, post_id):
        logging.info('Fetching post...')

        try:
            conn = self.conn
            cursor = conn.cursor()
            cursor.execute(sql_fetch_post, (post_id))

            post = cursor.fetchall()

            return post

        except Exception:
            logging.exception('get_post ---> error fetching post')
            return {}

    def get_posts(self, offset, fetch_next):
        logging.info('Fetching posts...')

        try:
            conn = self.conn
            cursor = conn.cursor()
            cursor.execute(sql_fetch_posts, (offset, fetch_next))

            posts = cursor.fetchall()

            return posts

        except Exception:
            logging.exception('get_posts ---> error fetching posts')
            return []

    def get_comments(self, post_id):
        logging.info('Fetching comments...')

        try:
            conn = self.conn
            cursor = conn.cursor()
            cursor.execute(sql_fetch_comments, (post_id))

            comments = cursor.fetchall()

            return comments

        except Exception:
            logging.exception('get_comments ---> error fetching comments')
            return []

    def close(self):
        if self.conn:
            self.conn.close()
