# Distance sensor

This is the description how to setup and run ultrasonic distance sensor HC-SR04 for Rapsberry Pi 4.

It also contains example data results gathered of this sensor.

## Wiring

Wire the sensor as described in the picture.

**Note**: the code uses pin GPIO23 as a Trig and GPIO24 as an Echo

Be careful about `Echo` pin, as it sends 5V signal, and Pi can handle only up to 3.3V on GPIO pins. Thus there is a need to make a votlage divider. For resistors I used 2.2k and 1.2k Ohm. For more info check [this site](https://thepihut.com/blogs/raspberry-pi-tutorials/hc-sr04-ultrasonic-range-sensor-on-the-raspberry-pi).

![alt text](https://tutorials-raspberrypi.com/wp-content/uploads/2014/05/ultraschall_Steckplatine-768x952.png "Logo Title Text 1")
source: [ThePiHut](https://thepihut.com/blogs/raspberry-pi-tutorials/27968772-turning-on-an-led-with-your-raspberry-pis-gpio-pins)

## Execute program

To start the program type

```bash
python distance-sensor.py
```

It will prompt you with the info on terminal, that it has started working and will display readouts of the sensor.

Also it will save those readouts to the `distance.csv` file in the same directory (note: it overwrites the file on the next execution).

## Examples

For the example readings you can go to [results](./results) folder. For now it contains two examples:

1. The person walking to the mirror in the straight line and moving to the side.
2. The person walking to the mirror from the side and after some time moving tho the side.

It also consists of graphs with visualization of that data and description of the particular phases.
