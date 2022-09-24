FROM tiangolo/uvicorn-gunicorn:python3.9-slim as base

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

WORKDIR /tmp

FROM base as build

RUN pip install poetry
RUN python -m venv /venv

COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt | /venv/bin/pip install -r /dev/stdin

COPY . .
RUN poetry build && /venv/bin/pip install dist/*.whl

FROM base as final

COPY --from=build /venv /venv
COPY docker-entrypoint.sh ./
COPY ./src ./src

RUN chmod +x ./docker-entrypoint.sh
CMD [ "./docker-entrypoint.sh" ]
