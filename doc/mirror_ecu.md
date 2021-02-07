# Smart Mirror ECU
For this Smart Mirror solution, for Electronic Control Unit (ECU) has been used For this Smart Mirror solution [Raspberry Pi 3bB](https://www.raspberrypi.org/products/raspberry-pi-3-model-b-plus/) was used as an Electronic Control Unit (ECU).

# Environment setup
## Hardware
### Camera
### Distance sensor
## Software
### Compile 
Install cmake by running command:
 
 `sudo apt-get install cmake`
### Installation of OpenCv
The installation steps for python OpenCv3 on Raspberry Pi:
```bash
sudo apt-get update && sudo apt-get upgrade
sudo reboot
mkdir ~/src && cd ~/src
wget https://bootstrap.pypa.io/get-pip.py
sudo python3 get-pip.py
sudo python3 -m pip install opencv-contrib-python
sudo pip install opencv-contrib-python
```

cd ~ && wget https://bootstrap.pypa.io/get-pip.py && sudo python get-pip.py