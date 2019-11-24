import logging

from sanic import Blueprint
from sanic.exceptions import SanicException
from sanic.request import Request
from sanic.response import HTTPResponse, json


bp = Blueprint('middleware')


CORS_HEADERS = {
    'access-control-allow-methods': 'GET, POST, DELETE, PUT, PATCH, OPTIONS',
    'access-control-allow-headers': 'Content-Type, api_key, Authorization, x-maxmind-city-id, x-maxmind-country-id, '
                                    'x-maxmind-geo-id',
    'access-control-allow-origin': '*'
}


@bp.middleware
def cors_request_middleware(request: Request):
    if request.method == 'OPTIONS':
        return HTTPResponse(status=200)


@bp.middleware('response')
def cors_response_middleware(_request: Request, response: HTTPResponse):
    response.headers.update(CORS_HEADERS)


@bp.exception(Exception)
def handle_server_error(request: Request, exception):
    if request is not None and exception is not None:
        message = "Internal server error"
        status_code = 500
        if isinstance(exception, SanicException):
            message = str(exception)
            status_code = exception.status_code

        body = request.json
        logging.exception(message, exc_info=exception, extra={
            'url': request.url,
            'method': request.method,
            'body': body,
            'status': status_code})

        return json({'error': message}, status=status_code)
