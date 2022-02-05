FROM python:3.10.1-slim-buster
SHELL ["/bin/bash", "-xe", "-o", "pipefail", "-c"]

RUN apt-get update
RUN apt-get install \
    'curl' \
    'ffmpeg' \
    'libsm6' \
    'libxext6' -y

ARG POETRY_HOME=/etc/poetry
ARG POETRY_VERSION=1.1.12

WORKDIR /app

COPY pyproject.toml poetry.lock poetry.toml ./

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 && \
  /etc/poetry/bin/poetry install

COPY . .

RUN chmod +x download_models.sh && source download_models.sh

EXPOSE 8080

ENV PATH "$PATH:/etc/poetry/bin"

CMD ["poetry", "run", "python", "main.py"]
