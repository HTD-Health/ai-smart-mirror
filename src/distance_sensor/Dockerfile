FROM alpine:edge

WORKDIR /app

ARG IMG_VERSION=v1.0.0 \
    USER=distance_sensor

ENV IMG_VERSION=${IMG_VERSION} \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

RUN addgroup -S ${USER} \
    && adduser -S ${USER} -G ${USER}

COPY ./requirements.txt /app

RUN apk update \
    && apk upgrade --no-cache musl \
    && apk add --no-cache build-base libzmq musl-dev python3 python3-dev zeromq-dev py3-pip \
    && apk add --no-cache raspberrypi-libs py3-rpigpio || : \
    && pip install --upgrade pip \
    && pip install -r requirements.txt \
    && apk del build-base musl-dev python3-dev zeromq-dev \
    && ln -s /usr/bin/python3 /usr/bin/python \
    && rm -rf /root/.cache /tmp/* \
    && find / | grep -E "(__pycache__|\.pyc|\.pyo$$)" | xargs rm -rf;

ARG PORT_OUT=${PORT_OUT:-5555} \
    EVENT_BUS_SERVER=${EVENT_BUS_SERVER:-event-bus} \
    TOPIC_OUT=${TOPIC_OUT:-3} \
    SLEEP=${SLEEP:-0.1} \
    DUMMY=${DUMMY:-} \
    TRIGGER_PIN=${TRIGGER_PIN:-16} \
    ECHO_PIN=${ECHO_PIN:-18} \
    THRESHOLD_DISTANCE=${THRESHOLD_DISTANCE:-80} \
    HADRCODED_DISTANCE=${HADRCODED_DISTANCE:-60} \
    SENSOR_SETTLE_TIME=${SENSOR_SETTLE_TIME:-0.3} \
    LOG_LEVEL=${LOG_LEVEL:-WARNING}

ENV PORT_OUT=${PORT_OUT} \
    EVENT_BUS_SERVER=${EVENT_BUS_SERVER} \
    TOPIC_OUT=${TOPIC_OUT} \
    SLEEP=${SLEEP} \
    TRIGGER_PIN=${TRIGGER_PIN} \
    ECHO_PIN=${ECHO_PIN} \
    DUMMY=${DUMMY} \
    THRESHOLD_DISTANCE=${THRESHOLD_DISTANCE} \
    HADRCODED_DISTANCE=${HADRCODED_DISTANCE} \
    SENSOR_SETTLE_TIME=${SENSOR_SETTLE_TIME} \
    LOG_LEVEL=${LOG_LEVEL}

EXPOSE ${PORT_IN} \
       ${PORT_OUT}

# Run as root to have access to distance_sensor FIXME: change permission to distance_sensor device
# USER ${USER}
COPY ./code/ /app
ENTRYPOINT [ \
        "sh", \
        "-c", \
        "if [ -z $DUMMY ]; \
            then python distance_sensor.py --event_bus_server=$EVENT_BUS_SERVER --port_out=$PORT_OUT --topic_out=$TOPIC_OUT --log_level=$LOG_LEVEL --trig $TRIGGER_PIN --echo $ECHO_PIN --sleep $SLEEP --thresholddistance $THRESHOLD_DISTANCE --sensorsettletime $SENSOR_SETTLE_TIME; \
            else python distance_sensor_dummy.py --event_bus_server=$EVENT_BUS_SERVER --port_out=$PORT_OUT --topic_out=$TOPIC_OUT --log_level=$LOG_LEVEL --sleep $SLEEP --sensorsettletime $SENSOR_SETTLE_TIME --hadrcodeddistance=$HADRCODED_DISTANCE; \
        fi" \
    ]
