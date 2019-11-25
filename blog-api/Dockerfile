FROM python:3.7

RUN apk add --no-cache build-base
RUN pip install pipenv==2018.11.26 pip==19.3.1

WORKDIR /app
ADD Pipfile ./
ADD Pipfile.lock ./
ARG DEV_BUILD

RUN pipenv install --system --deploy -v $DEV_BUILD
EXPOSE 8000
ENV PYTHONUNBUFFERED 1

CMD ["python", "main.py"]

ADD ./blog-api ./