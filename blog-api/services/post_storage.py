from sanic import Blueprint
import sqlite3
import time

import logging

# FOR DEMO ONLY:
from faker import Faker
from random import randint


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
                        where id = ?'''

sql_fetch_posts = '''select *
                        from posts
                        offset ? rows
                        fetch next ? rows only
                        order by created_time desc'''

sql_fetch_comments = '''select *
                            from comments
                            where post_id = ?
                            order by created_time desc'''


class PostStorage:

    def init(self):
        self.conn = None
        try:
            self.conn = sqlite3.connect(':memory:')
            cursor = self.conn.cursor()
            cursor.execute(create_posts_table)
            cursor.execute(create_comments_table)
        except Exception:
            raise Exception('Failed to set up in-memory database')

        # Seed demo entries (DEMO PURPOSES ONLY):
        err = self.seed_demo_db()
        if err:
            raise Exception('Failed to seed demo database')

    def get_post(self, post_id):
        logging.info('Fetching post...')

        try:
            cursor = self.conn.cursor()
            cursor.execute(sql_fetch_post, (post_id,))

            post = cursor.fetchone()

            return post

        except Exception:
            logging.exception('get_post ---> error fetching post')
            return {}

    def get_posts(self, offset, fetch_next):
        logging.info('Fetching posts...')

        try:
            cursor = self.conn.cursor()
            cursor.execute(sql_fetch_posts, (offset, fetch_next))

            posts = cursor.fetchall()

            return posts

        except Exception:
            logging.exception('get_posts ---> error fetching posts')
            return []

    def get_comments(self, post_id):
        logging.info('Fetching comments...')

        try:
            cursor = self.conn.cursor()
            cursor.execute(sql_fetch_comments, (post_id,))

            comments = cursor.fetchall()

            return comments

        except Exception:
            logging.exception('get_comments ---> error fetching comments')
            return []

    def close(self):
        if self.conn:
            self.conn.close()

    # FOR DEMO ONLY:
    def seed_demo_db(self):
        logging.info('Initializing demo db seed...')

        cursor = self.conn.cursor()

        fake = Faker()
        fake_posts = []

        sql_seed_posts = '''insert into posts(id, author, title, text, created_time)
                            values(?, ?, ?, ?, ?)'''
        sql_seed_comments = '''insert into comments(id, post_id, author, text, created_time)
                            values(?, ?, ?, ?, ?)'''

        # *For demo purposes, ids will be random integers for simplicity.

        for i in range(50):
            fake_post_id = i + 100000
            fake_post_author = fake.name()
            fake_post_title = fake.sentence()
            fake_post_text = fake.text()
            post_created_time = time.time()

            try:
                cursor.execute(sql_seed_posts,
                               (fake_post_id,
                                fake_post_author,
                                fake_post_title,
                                fake_post_text,
                                post_created_time))
            except Exception:
                raise Exception('seeding demo posts failed')

        for j in range(150):
            fake_comment_id = j + 1000
            related_post_id = randint(100000, 100050)
            fake_comment_author = fake.name()
            fake_comment_text = fake.text()
            comment_created_time = time.time()

            try:
                cursor.execute(sql_seed_comments,
                               (fake_comment_id,
                                related_post_id,
                                fake_comment_author,
                                fake_comment_text,
                                comment_created_time))
            except Exception:
                raise Exception('seeding demo comments failed')

        logging.info('Demo db seeding complete.')
