FROM tiangolo/uvicorn-gunicorn:python3.9-slim as requirements-stage

WORKDIR /tmp

RUN pip install poetry
COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM tiangolo/uvicorn-gunicorn:python3.9-slim
ENV PATH /home/${USERNAME}/.local/bin:${PATH}
COPY --from=requirements-stage /tmp/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt
COPY ./src ./src

ENV PORT=8000
EXPOSE 80

CMD ["python", "src.main.py"]
