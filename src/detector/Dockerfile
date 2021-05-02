FROM alpine:edge

WORKDIR /app

ARG IMG_VERSION=v1.0.0 \
    USER=camera

ENV IMG_VERSION=${IMG_VERSION} \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

RUN addgroup -S ${USER} \
    && adduser -S ${USER} -G ${USER}

COPY ./requirements.txt /app

RUN apk update \
    && apk upgrade --no-cache musl \
    && apk add --no-cache build-base libzmq musl-dev python3 python3-dev zeromq-dev py3-pip \
    && apk add --no-cache raspberrypi-libs || : \
    && pip install --upgrade pip \
    && pip install -r requirements.txt \
    && apk del build-base musl-dev python3-dev zeromq-dev \
    && ln -s /usr/bin/python3 /usr/bin/python \
    && rm -rf /root/.cache /tmp/* \
    && find / | grep -E "(__pycache__|\.pyc|\.pyo$$)" | xargs rm -rf;

ARG PORT_IN=${PORT_IN:-5556} \
    EVENT_BUS_SERVER=${EVENT_BUS_SERVER:-event-bus} \
    TOPIC_IN=${TOPIC_IN:-2} \
    MODEL_DIR=${MODEL_DIR:-/tmp/models}
    IMAGE_DIR=${IMAGE_DIR:-/tmp/images} \
    LOG_LEVEL=${LOG_LEVEL:-WARNING}

ENV PORT_IN=${PORT_IN} \
    EVENT_BUS_SERVER=${EVENT_BUS_SERVER} \
    TOPIC_IN=${TOPIC_IN} \
    MODEL_DIR=${MODEL_DIR} \
    IMAGE_DIR=${IMAGE_DIR} \
    LOG_LEVEL=${LOG_LEVEL} \
    READTHEDOCS=True

EXPOSE ${PORT_IN} \
       ${PORT_OUT}

# Run as root to have access to camera FIXME: change permission to model device
# USER ${USER}
COPY ./code/ /app
ENTRYPOINT ["sh", "-c", "python camera.py --event_bus_server=$EVENT_BUS_SERVER --port_in=$PORT_IN --topic_in=$TOPIC_IN --log_level=$LOG_LEVEL --model_dir=$MODEL_DIR --image_dir=$IMAGE_DIR"]
