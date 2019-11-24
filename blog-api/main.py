from sanic import Sanic

import config


def main():
    app = Sanic('blog-api')

    app.run(host='0.0.0.0', post=config.LISTEN_PORT)


if __name__ == "__main__":
    main()
