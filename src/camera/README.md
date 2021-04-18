# Camera module


## Running on raspberry
```
sudo docker pull 573518775438.dkr.ecr.us-east-2.amazonaws.com/smart-mirror-camera:latest
# run newest image
sudo docker run --privileged -v /tmp/images:/tmp/images --env LD_LIBRARY_PATH=/opt/vc/lib 573518775438.dkr.ecr.us-east-2.amazonaws.com/smart-mirror-camera
```
If something isn't working take a look to `Run` section on [README](README.md) file.

## Testing

```bash
# run event bus
docker-compose up event-bus

# run camera module
python run.py --image_dir=`pwd`

# send event to make a picture
python src/utils/send_event.py 1 ''
```


### CrossArch build
More info about [buildx](https://docs.docker.com/docker-for-mac/multi-arch/)
```sh
# login to aws
/usr/local/bin/aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 573518775438.dkr.ecr.us-east-2.amazonaws.com

# prepare buildx (needed once)
docker buildx create --name smartmirror
docker buildx use smartmirror
docker buildx inspect --bootstrap

# Build images for amd64, arm64 and arm/v7 architectures
docker buildx build --platform linux/amd64,linux/arm64,linux/arm/v7 .

# with upload to AWS ECR
docker buildx build --platform linux/amd64,linux/arm64,linux/arm/v7 -t 573518775438.dkr.ecr.us-east-2.amazonaws.com/smart-mirror-camera:latest --push .

# and confirm the exported images are correctly uploaded
docker buildx imagetools inspect 573518775438.dkr.ecr.us-east-2.amazonaws.com/smart-mirror-camera:latest
```
