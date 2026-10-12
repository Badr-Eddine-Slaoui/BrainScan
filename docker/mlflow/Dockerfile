FROM python:3.12-slim

ARG APP_UID=1000
ARG APP_GID=1000

ENV PYTHONUNBUFFERED=1

COPY requirements/mlflow/requirements.txt .
RUN pip install -r ./requirements.txt

RUN groupadd --gid ${APP_GID} mlflow \
    && useradd --uid ${APP_UID} --gid ${APP_GID} --create-home mlflow \
    && mkdir -p /mlflow/artifacts \
    && chown -R ${APP_UID}:${APP_GID} /mlflow

USER mlflow
WORKDIR /mlflow