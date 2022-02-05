FROM python:3.10.1-slim
SHELL ["/bin/bash", "-xe", "-o", "pipefail", "-c"]

RUN apt-get update && apt-get install -y curl

ARG POETRY_HOME=/etc/poetry
ARG POETRY_VERSION=1.1.12

WORKDIR /app

COPY pyproject.toml poetry.lock poetry.toml ./

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 && \
  /etc/poetry/bin/poetry install


COPY . .

EXPOSE 8000

ENV PATH "$PATH:/etc/poetry/bin"

CMD ["poetry", "run", "streamlit", "run", "main.py"]

