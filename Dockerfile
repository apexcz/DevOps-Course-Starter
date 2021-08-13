FROM python:3.9.6-slim-buster as parent

RUN apt-get update && apt-get install -y curl && \
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

ENV PATH="/root/.poetry/bin:${PATH}"

WORKDIR /app

COPY pyproject.toml /app/

RUN  poetry install --no-dev --no-root

COPY . /app

EXPOSE 5000



FROM parent as development 

ENTRYPOINT poetry run flask run --host=0.0.0.0



FROM parent as production

ENTRYPOINT poetry run gunicorn --workers=2 --bind=0.0.0.0:5000 'todo_app.app:create_app()'