# Thermovision sensor (MLX90641)

How to start?

1. Connect sensor with raspberry pi
   ![sensor conection to rp pi](https://images.squarespace-cdn.com/content/v1/59b037304c0dbfb092fbe894/1591731759228-C66M7BWPEH5KPK3UYZ9A/ke17ZwdGBToddI8pDm48kL0aU6AQOwPnD5bbw5AxIml7gQa3H78H3Y0txjaiv_0fDoOvxcdMmMKkDsyUqMSsMWxHk725yiiHCCLfrh8O1z4YTzHvnKhyp6Da-NYroOW3ZGjoBKy3azqku80C789l0ldnepkVHAptGDUshypSjuZyJSo6UXQu3jq1vLDMsMGe5B2oEJkekO2SJjQQAHY12w/mlx90640_rpi_wiring_diagram_w_table.png?format=2500w)

2. Install I2C tools:
   `sudo apt-get install -y python-smbus`
   `sudo apt-get install -y i2c-tools`

3. Enable I2C in raspberry pi boot config
   `sudo nano /boot/config.txt`

   Find line `dtparam=i2c_arm=on` and uncomment, after that reboot `sudo reboot`

4. Install mlx python library `pip3 install seeed-python-mlx9064x` and numpy `pip3 install numpy`

5. Run `python3 thermovision_sensor.py -t` to test
