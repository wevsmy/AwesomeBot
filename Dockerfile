FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

RUN python3 -m pip config set global.index-url https://mirrors.aliyun.com/pypi/simple

RUN python3 -m pip install poetry && poetry config virtualenvs.create false

COPY ./.env.prod ./bot.py ./pyproject.toml ./poetry.lock* /app/

COPY ./src /app/src

RUN poetry install --no-root --no-dev