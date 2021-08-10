# FROM pytorch/pytorch:1.9.0-cuda10.2-cudnn7-runtime
FROM nvidia/cuda:10.1-cudnn7-runtime

RUN apt update && \
    apt install --no-install-recommends -y build-essential software-properties-common && \
    add-apt-repository -y ppa:deadsnakes/ppa && \
    apt install --no-install-recommends -y python3.8 python3-pip python3-setuptools python3-distutils && \
    apt clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /requirements.txt

COPY . /src

RUN python3.8 -m pip install --upgrade pip && \
    python3.8 -m pip install --no-cache-dir -r /requirements.txt

CMD ["/src/ecu.py"]
ENTRYPOINT ["python3.8"]
