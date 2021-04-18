# Distance sensor

This is the description of how to set up and run ultrasonic distance sensor HC-SR04 for Raspberry Pi 3.

It also contains example data results gathered from this sensor.

## Wiring

Wire the sensor as described in the picture.

**Note**: the code uses pin GPIO23 as a Trig and GPIO24 as an Echo

Be careful about the `Echo` pin, as it sends the 5V signal, and Pi can handle only up to 3.3V on GPIO pins. Thus, there is a need
to make a voltage divider, reducing the voltage into the acceptable range. For resistors, I used 2.2k and 1.2k Ohm. For more info
check [this site](https://thepihut.com/blogs/raspberry-pi-tutorials/hc-sr04-ultrasonic-range-sensor-on-the-raspberry-pi)
.

![alt text](https://tutorials-raspberrypi.com/wp-content/uploads/2014/05/ultraschall_Steckplatine-768x952.png "RPi distance sensor set up diagram")
source: [tutorials-raspberrypi.com](https://tutorials-raspberrypi.com/raspberry-pi-ultrasonic-sensor-hc-sr04/)

## Execute program

To start the program type

```bash
python distance_sensor.py
```

It will prompt you with the info on terminal, that it has started working and will display readouts of the sensor.

Also, it will save those readouts to the `distance.csv` file in the same directory (note: it overwrites the file on the
next execution).

## Examples

For the example readings you can go to [results](results) folder. For now, it contains two examples:

1. The person walking to the mirror in the straight line and moving to the side.
2. The person walking to the mirror from the side and after some time moving to the side.

It also consists of graphs with visualization of that data and description of the particular phases.

### CrossArch build
More info about [buildx](https://docs.docker.com/docker-for-mac/multi-arch/).
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
docker buildx build --platform linux/amd64,linux/arm64,linux/arm/v7 -t 573518775438.dkr.ecr.us-east-2.amazonaws.com/smart-mirror-distance-sensor:latest --push .

# and confirm the exported images are correctly uploaded
docker buildx imagetools inspect 573518775438.dkr.ecr.us-east-2.amazonaws.com/smart-mirror-distance-sensor:latest
```
