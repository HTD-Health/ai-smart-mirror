FROM python:3.8-slim
# pytorch/pytorch
# 

WORKDIR /app

ARG IMG_VERSION=v1.0.0 \
    USER=detector

ENV IMG_VERSION=${IMG_VERSION} \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

RUN addgroup --system ${USER} \
    && adduser --system --group ${USER}

COPY ./requirements.txt /app 

RUN echo "|---> Update system" \
    && apt-get update \
    && apt-get install build-essential musl-dev \
    && apt-get upgrade musl \
    && apt-get install raspberrypi-libs || : \
    # Resolving installation problems with pyzmq
    && echo "|---> Install req's for pyzmq" \
    && apt-get -y install gcc mono-mcs \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --upgrade pip setuptools wheel \
    && pip install p5py \
    && pip install PEP517 \
    # && add-apt-repository ppa:chris-lea/zeromq \
    # && apt-get update \
    && apt-get install libzmq3-dbg libzmq3-dev libzmq3 \
    && echo "|---> Install Python libs" \
    && pip install --upgrade pip \
    # && pip install pyzmq \
    && pip install -r requirements.txt --no-binary :all: \
    && echo "|---> Create symbolic links" \ 
    && ln -s /usr/bin/python3 /usr/bin/python \
    && echo "|---> Cleaning" \
    # && apt-get remove build-base musl-dev zeromq-dev \
    && rm -rf /root/.cache /tmp/* \
    && find / | grep -E "(__pycache__|\.pyc|\.pyo$$)" | xargs rm -rf;

ARG PORT_IN=${PORT_IN:-5556} \
    EVENT_BUS_SERVER=${EVENT_BUS_SERVER:-event-bus} \
    TOPIC_IN=${TOPIC_IN:-2} \
    MODEL_DIR=${MODEL_DIR:-/-/tmp/models} \
    IMAGE_DIR=${IMAGE_DIR:-/-/tmp/images} \
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

# Run as root to have access to detector FIXME: change permission to model device
# USER ${USER}
COPY ./code/ /app

# Install mask model
# USER root
COPY lib/ai-mask-model ai-mask-model
RUN echo "|---> Installing Mask Model" \
    && pip install --no-cache-dir -e ai-mask-model/. -f https://download.pytorch.org/whl/torch_stable.html

# RUN echo "|---> Install additional tools" \
#     && apt add git \
#     && apt add cmake cmake-doc extra-cmake-modules extra-cmake-modules-doc \
#     && echo "|---> Install PyTorch" \
#     && git clone --recursive https://github.com/pytorch/pytorch \
#     && cd pytorch && python setup.py install \
#     && echo "|---> Install PyTorchLightning" \
#     && git clone --recursive https://github.com/pytorchlightning/pytorch-lightning \
#     && cd pytorch-lightning && python setup.py install \
#     && echo "|---> Cleaning" \
#     && rm -rf /pytorch \
#     && rm -rf /pytorch-lightning \

USER root
ENTRYPOINT ["sh", "-c", "python detector.py --event_bus_server=$EVENT_BUS_SERVER --port_in=$PORT_IN --topic_in=$TOPIC_IN --log_level=$LOG_LEVEL --model_dir=$MODEL_DIR --image_dir=$IMAGE_DIR"]

