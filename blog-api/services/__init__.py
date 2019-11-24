import logging

from sanic import Blueprint

from services.post_storage import PostStorage

bp = Blueprint('services')


@bp.listener('before_server_start')
def attach(app, _):
    logging.info('Initializing external dependencies layer')
    app.services = ExternalDependencies()


class ExternalDependencies:
    post_storage: PostStorage
