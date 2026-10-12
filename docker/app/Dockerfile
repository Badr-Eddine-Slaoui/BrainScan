FROM python:3.11-slim

ARG APP_UID=1000
ARG APP_GID=1000

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/opt/project \
    PIP_NO_CACHE_DIR=1 \
    HOME=/home/appuser

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
        libgl1 \
        libglib2.0-0 \
        libsm6 \
        libxrender1 \
        libxext6 \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd --gid ${APP_GID} appuser \
    && useradd --uid ${APP_UID} --gid ${APP_GID} --create-home --home-dir /home/appuser appuser \
    && mkdir -p /opt/project \
    && chown -R ${APP_UID}:${APP_GID} /opt/project /home/appuser

WORKDIR /opt/project

COPY requirements/app/requirements.txt requirements/app/requirements.txt
RUN pip install -r requirements/app/requirements.txt

COPY --chown=${APP_UID}:${APP_GID} . .

USER appuser

CMD ["tail", "-f", "/dev/null"]