from sanic import Sanic

import logging
import config
import middleware
import services
from methods import status, post


def main():
    app = Sanic('blog-api')

    # Infrastructure
    app.blueprint(middleware.bp)
    app.blueprint(services.bp)

    # Services
    app.blueprint(services.post_storage.bp)

    # Methods
    app.blueprint(status.bp)
    #app.blueprint(post.bp)

    # Set root logging level
    logging.getLogger().setLevel(logging.INFO)

    app.run(host='0.0.0.0', port=config.LISTEN_PORT)


if __name__ == "__main__":
    main()
