# weather-monitor

## Introduction
A weather monitor using a Raspberry Pi, BMP085 and DHT22 sensor, uploading to IoT platform ThingSpeak and Slack using their web apis.
https://au.mathworks.com/help/thingspeak/update-a-channel.html
https://github.com/raddevon/pyspeak

## Todo
1. After you've got it working you could set the filesystem to read only to save SD card wear
(https://hallard.me/raspberry-pi-read-only/, or like me just disable swap and log to RAM:
http://raspberrypi.stackexchange.com/questions/169/how-can-i-extend-the-life-of-my-sd-card)

2. Incorporate Shinyei PPD42NS air quality into IoT platform

## Hardware
Tested on: Rapsberry Pi Model A (original)  
Adafruit BMP085 temp and pressure sensor

- VCC -> 3.3v
- GND -> GND
- SCL -> GPIO 03
- SDA -> GPIO 02

DHT22 temp and humidity sensor
pin 1 / GND must have a voltage divider to reduce 5v to 3.3v

- pin 1 -> 3.3v
- pin 2 -> GPIO 08 (inside sensor connected to GPIO07)
- pin 3 -> NONE
- pin 4 => GND

Shinyei PPD42NS particle sensor
pin 1 / GND must have a voltage divider to reduce 5v to 3.3v

- pin + -> 3.3v
- pin 2 -> GPIO 07
- pin - -> GND


## Accounts
You'll need a thingspeak account, and to create a channel with three fields, and get your API key
You'll need a slack account, and to get your API key

## Installation
1. Starting with Raspbian Jessie Lite, update the system, :

``` bash
sudo apt-get update
sudo apt-get install python-dev python-pip git
``` 

2. Enable i2c by: sudo raspi-config and Advanced Options > I2C > Enable
And whilst you're in the config program, change your timezone
Exit and reboot

3. Clone this repo and the BMP085 repo:
``` bash
git clone https://github.com/andy-pi/weather-monitor.git
git clone https://github.com/adafruit/Adafruit_Python_BMP.git
cd Adafruit_Python_BMP
sudo python setup.py install
```


4. Install PIGPIO, a library for low level GPIO operations (this repo includes DHT22.py)
(http://abyz.co.uk/rpi/pigpio/)
``` bash
wget abyz.co.uk/rpi/pigpio/pigpio.zip
unzip pigpio.zip
cd PIGPIO
make
sudo make install
```

5. Install Python Slack Api wrapper:
```bash
sudo pip install slacker
```

6. Update root crontab with the following lines to run the thingspeak script every 15 mins and slack update daily:
``` bash
@reboot /usr/local/bin/pigpiod
@reboot sntp -s 24.56.178.140 # to force time update on reboot
0,15,30,45 * * * * python /home/pi/weather-monitor/thingspeak_update.py # for logging add >> /home/pi/weather-monitor/log 2>&1
30 6 * * * python /home/pi/weather-monitor/slack_update.py
```

# Air Quality - Shinyei PPD42NS only

## Basic Printout of air quality

Carry out steps 1-4 above and then:  

```bash
sudo pigpiod
python air_quality.py
```

The output will be printed on screen. Note that the instantaneous AQI is not actually correct, it should be taken as a 24 average of the PM2.5 particles in micrograms/m3