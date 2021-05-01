from thermovision_sensor import ThermovisionSensor


"""It allows you to check the correctness of the configuration
and connection of the sensor.

The function returns 10 average temperature values for an object
with a temperature close to human temperature
"""
def main():
    thermal_sensor = ThermovisionSensor()
    for i in range(10):
        print(thermal_sensor.get_temperature())


if __name__ == '__main__':
    main()
