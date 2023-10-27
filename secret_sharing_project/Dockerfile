FROM python:3.11.0-alpine

ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=secret_sharing_project.settings

WORKDIR /app

COPY requirements.txt /app/

RUN apk add --update --no-cache \
    postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
    python3-dev \
    libffi-dev \
    postgresql \
    ca-certificates \
    build-base  \
    postgresql-dev \
    gcc \
    musl-dev \
    zlib \
    zlib-dev \
    libpq-dev \
    libpq \
    coreutils \
    dpkg-dev dpkg \
    make \
    openssl-dev \
    linux-headers

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

RUN apk del .tmp-build-deps

COPY . /app

EXPOSE 3030
