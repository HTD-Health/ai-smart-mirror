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
    && READTHEDOCS=True pip install picamera==1.13 \
    && pip install --upgrade pip \
    # && pip install opencv-python==4.5.1.48 \
    && pip install -r requirements.txt \
    && apk del build-base musl-dev python3-dev zeromq-dev \
    && ln -s /usr/bin/python3 /usr/bin/python \
    && rm -rf /root/.cache /tmp/* \
    && find / | grep -E "(__pycache__|\.pyc|\.pyo$$)" | xargs rm -rf;

ARG PORT_IN=${PORT_IN:-5556} \
    PORT_OUT=${PORT_OUT:-5555} \
    EVENT_BUS_SERVER=${EVENT_BUS_SERVER:-event-bus} \
    TOPIC_IN=${TOPIC_IN:-1} \
    TOPIC_OUT=${TOPIC_OUT:-2} \
    IMAGE_HEIGHT=${IMAGE_HEIGHT:-768} \
    IMAGE_WIDTH=${IMAGE_WIDTH:-1024} \
    IMAGE_FORMAT=${IMAGE_FORMAT:-jpg} \
    IMAGE_DIR=${IMAGE_DIR:-/tmp/images} \
    LOG_LEVEL=${LOG_LEVEL:-WARNING}

ENV PORT_IN=${PORT_IN} \
    PORT_OUT=${PORT_OUT} \
    EVENT_BUS_SERVER=${EVENT_BUS_SERVER} \
    TOPIC_IN=${TOPIC_IN} \
    TOPIC_OUT=${TOPIC_OUT} \
    IMAGE_HEIGHT=${IMAGE_HEIGHT} \
    IMAGE_WIDTH=${IMAGE_WIDTH} \
    IMAGE_FORMAT=${IMAGE_FORMAT} \
    IMAGE_DIR=${IMAGE_DIR} \
    LOG_LEVEL=${LOG_LEVEL} \
    READTHEDOCS=True

EXPOSE ${PORT_IN} \
       ${PORT_OUT}

# Run as root to have access to camera FIXME: change permission to camera device
# USER ${USER}
COPY ./code/ /app
ENTRYPOINT ["sh", "-c", "python camera.py --event_bus_server=$EVENT_BUS_SERVER --image_format=$IMAGE_FORMAT --image_dir=$IMAGE_DIR --image_height=$IMAGE_HEIGHT --image_width=$IMAGE_WIDTH --port_in=$PORT_IN --port_out=$PORT_OUT --topic_in=$TOPIC_IN --topic_out=$TOPIC_OUT --log_level=$LOG_LEVEL"]
