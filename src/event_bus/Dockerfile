FROM alpine:edge

WORKDIR /app

ARG IMG_VERSION=v1.0.0 \
    USER=event_bus

ENV IMG_VERSION=${IMG_VERSION} \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

RUN addgroup -S ${USER} \
    && adduser -S ${USER} -G ${USER}

COPY ./requirements.txt /app

RUN apk update \
    && apk upgrade --no-cache musl \
    && apk add build-base --no-cache libzmq musl-dev python3 python3-dev zeromq-dev py3-pip \
    && pip install --upgrade pip \
    && pip install -r requirements.txt \
    && apk del build-base musl-dev python3-dev zeromq-dev \
    && ln -s /usr/bin/python3 /usr/bin/python \
    && rm -rf /root/.cache /tmp/* \
    && find / | grep -E "(__pycache__|\.pyc|\.pyo$$)" | xargs rm -rf;

ARG PORT_IN=${PORT_IN:-5555} \
    PORT_OUT=${PORT_OUT:-5556} \
    LOG_LEVEL=${LOG_LEVEL:-WARNING}

ENV PORT_IN=${PORT_IN} \
    PORT_OUT=${PORT_OUT} \
    LOG_LEVEL=${LOG_LEVEL}

EXPOSE ${PORT_IN} \
       ${PORT_OUT}

USER ${USER}
COPY ./code/ /app
ENTRYPOINT ["sh", "-c", "python event_bus.py --port_in=$PORT_IN --port_out=$PORT_OUT --log_level=$LOG_LEVEL"]
