#!/usr/bin/python2.7

# Title:  Slack RaspberryPi Weather station
# Author: AndyPi
# Date:   29th Feb 2016
# Rev:    1

# Hardware
# DHT22 (temp / humidity)
# BMP085 (temp/atmospheric pressure)
# (air quality)

# Todo:
# add other sensors

# import libraries
import sys, time, Adafruit_BMP.BMP085, DHT22, pigpio, atexit, config
BMP085sensor=Adafruit_BMP.BMP085.BMP085()
from config import *
from slacker import Slacker

# Setup RPi GPIO pins
PIN_DHT22=8
PIN_BMP085_SDA=0
PIN_BMP085_SCL=0
PIN_TGS2600=0

# Setup constants
slack = Slacker(SLACKAPI)

# main loop
if __name__ == "__main__":

	pi = pigpio.pi()

	# Humidity and temp from DHT22
	s = DHT22.sensor(pi, PIN_DHT22, LED=None, power=8)   
	s.trigger()
	time.sleep(0.2)
	humidity=s.humidity()
	temp1=s.temperature()
	
	# temp and pressure from BMP085
	temp2=BMP085sensor.read_temperature()
	pressure = BMP085sensor.read_pressure()
	hpapressure=pressure/100
	# calc average temp of 2 sensors
	temperature = 0
	temperature=(temp1+temp2)/2
	tempf=(temperature*9/5)+32
	# get reading from air quality sensor
	#airq = 

	msgstring = "Good Morning! Here's today's current weather:" + "\nTemp: " + str(temperature) + "C or " + str(tempf)+ "F\nRelative Humidity: " + str(humidity) + "%\nPressure: " + str(hpapressure) + "hPa"	
	
	slack.chat.post_message('#weather', msgstring)
	pi.stop()
	sys.exit()

