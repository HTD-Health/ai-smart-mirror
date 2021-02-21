# Event bus implementation as separate docker container

This app is responsible for holding SmartMirror event bus, and distributing events, like `proximity sensor noticed someone in front of the mirror` or `mask ok`, between multiple modules/containers. It is build on top of [zeroMQ](https://pyzmq.readthedocs.io/en/latest/), uses its own container with in/out ports exposed

Look into examples folder for example producer and consumer codes with message filtering

Exposed ports (default), each module that produces event should connect to **Incoming port**, and each listening to **Outgoing port**
- Incoming events port: 5555
- Outgoing events port: 5556

## Build and run

You can build an images for local machine or multiple architectures, depending on your needs.

### CrossArch build
More info about [buildx](https://docs.docker.com/docker-for-mac/multi-arch/)
```sh
# prepare buildx (needed once)
docker buildx create --name smartmirror
docker buildx use smartmirror
docker buildx inspect --bootstrap
# Build images for amd64, arm64 and arm/v7 architectures
docker buildx build --platform linux/amd64,linux/arm64,linux/arm/v7 .

# with upload to AWS ECR
docker buildx build --platform linux/amd64,linux/arm64,linux/arm/v7 -t 573518775438.dkr.ecr.us-east-2.amazonaws.com/smart-mirror-event-bus:latest --push .

# and confirm the exported images are correctly uploaded
docker buildx imagetools inspect 573518775438.dkr.ecr.us-east-2.amazonaws.com/smart-mirror-event-bus:latest
```

### Local build
```sh
# build and tag
docker build -t smart-mirror-event-bus .
# or build with custom ports and log level as defaults
docker build --build-arg LOG_LEVEL=debug --build-arg PORT_IN=5500 --build-arg PORT_OUT=5501 -t smart-mirror-event-bus .

# run with port mapping
docker run -p 5555:5555 -p 5556:5556 smart-mirror-event-bus:latest

# or with custom ports and log level
docker run -p 5500:5500 -p 5501:5501 --env PORT_IN=5500 --env PORT_OUT=5501 --env LOG_LEVEL=debug smart-mirror-event-bus:latest
```
