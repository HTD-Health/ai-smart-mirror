FROM ubuntu:18.04

WORKDIR /app

USER root

ENV PYTHONUNBUFFERED TRUE \
    PYTHONPATH=/app

COPY ./requirements.txt /app

RUN apk update \
    && apk upgrade --no-cache musl \
    && apk add --no-cache build-base libzmq musl-dev python3 python3-dev zeromq-dev py3-pip \
    && pip install --upgrade pip \
    && apk del build-base musl-dev python3-dev zeromq-dev \
    && ln -s /usr/bin/python3 /usr/bin/python \
    && rm -rf /root/.cache /tmp/* \
    && find / | grep -E "(__pycache__|\.pyc|\.pyo$$)" | xargs rm -rf;

RUN pip install --no-cache-dir -r requirements.txt -f https://download.pytorch.org/whl/torch_stable.htm

COPY ./code/ /app
ENTRYPOINT ["sh", "-c", "python ecu.py"]
