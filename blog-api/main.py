from sanic import Sanic

import config

import services


def main():
    app = Sanic('blog-api')

    # Infrastructure
    app.blueprint(services.bp)

    # Services
    app.blueprint(services.post_storage.bp)

    app.run(host='0.0.0.0', post=config.LISTEN_PORT)


if __name__ == "__main__":
    main()
