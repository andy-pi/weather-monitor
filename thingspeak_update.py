#!/usr/bin/python2.7

# Title:  ThingSpeak / RaspberryPi Weather station
# Author: AndyPi

# Hardware
# DHT22 (temp / humidity)
# BMP085 (temp/atmospheric pressure)
# (air quality)

# Todo:
# add other sensors
# rpi sd card hardeneing

# import libraries
import sys, httplib, urllib, time, Adafruit_BMP.BMP085, DHT22, pigpio, atexit
BMP085sensor=Adafruit_BMP.BMP085.BMP085()
from config import *

# Setup RPi GPIO pins
PIN_DHT22=8
PIN_DHT22i=7
PIN_BMP085_SDA=0
PIN_BMP085_SCL=0
PIN_TGS2600=0


# update thingspeak routine (max once every 15 seconds)
def update_thingspeak(data1, data2, data3, data4):
	params = urllib.urlencode({"field1": data1, "field2": data2, "field3": data3, "field4": data4,'key':THINGSPEAK_APIWRITE})
	headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
	conn = httplib.HTTPConnection("api.thingspeak.com:80")                
	try:
		conn.request("POST", "/update", params, headers)
		#response = conn.getresponse()
		#print response.status, response.reason
		#data = response.read()
		conn.close()
	except:
		pass
		# error handler if needed


# main loop
if __name__ == "__main__":

	pi = pigpio.pi()

	# Humidity and temp from DHT22 (outisde)
	s = DHT22.sensor(pi, PIN_DHT22, LED=None, power=8)   
	s.trigger()
	time.sleep(0.2)
	humidity=s.humidity()
	temp1=s.temperature()
	
	si = DHT22.sensor(pi, PIN_DHT22i, LED=None, power=8)   
	si.trigger()
	time.sleep(0.2)
	humidityi=si.humidity()
	
	# temp and pressure from BMP085
	temp2=BMP085sensor.read_temperature()
	pressure = BMP085sensor.read_pressure()

	# calc average temp of 2 sensors
	temperature = 0
	temperature=(temp1+temp2)/2
	
	# get reading from air quality sensor
	#airq = 

	update_thingspeak(temperature, humidity, pressure, humidityi)#, airq)
	print "Temp (DHT22) " + str(temp1)
	print "Temp (BMP)" + str(temp2)
	print "Humidity (outide): " + str(humidity)
	print "Humidity (inside): " + str(humidityi)
	print "Pressure: " + str(pressure)	
	
	sys.exit()