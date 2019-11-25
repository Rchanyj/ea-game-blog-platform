import os

# App

LISTEN_PORT = int(os.getenv('LISTEN_PORT', 8000))
SWAGGER_HOST = os.getenv('SWAGGER_HOST')
