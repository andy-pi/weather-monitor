# weather-monitor

## Todo
Remove all logging in Raspbian to reduce SD card writes and give logevity
Add dust sensor module PPD42NS

## Hardware
Rapsberry Pi Model A (original)
Adafruit BMP085 temp and pressure sensor
DHT22 temp and humidity sensor

## Installation
Clone this repo and the BMP085 repo:
``` bash
git clone https://github.com/andy-pi/weather-monitor.git
git clone https://github.com/adafruit/Adafruit_Python_BMP.git

```

Install PIGPIO, a library for low level GPIO operations (this repo includes DHT22.py)
(http://abyz.co.uk/rpi/pigpio/)
``` bash
wget abyz.co.uk/rpi/pigpio/pigpio.zip
unzip pigpio.zip
cd PIGPIO
make
sudo make install
sudo pigpiod
```

Update root crontab with the following lines to start pigpiod start on boot and the script to run every 15 mins:
``` bash
@reboot pigpiod
0,15,30,45 * * * * /home/pi/humidityapp/app.py # for logging add >> /home/pi/humidityapp/log 2>&1
```

