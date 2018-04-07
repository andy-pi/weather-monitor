#!/usr/bin/python2.7

# Title:  ThingSpeak / RaspberryPi Weather station
# Author: AndyPi

# Hardware:
# DHT22 (temp / humidity)
# BMP085 (temp/atmospheric pressure)
# Shinyei PPD42NS Dust Sensor (air quality)


# import libraries
import sys, httplib, urllib, time, Adafruit_BMP.BMP085, DHT22, pigpio, atexit
from collections import deque
BMP085sensor=Adafruit_BMP.BMP085.BMP085()
from config import *
import air_quality

# Setup RPi GPIO pins
PIN_DHT22=8
PIN_PPD42NS=7
#PIN_DHT22i=7
PIN_BMP085_SDA=0
PIN_BMP085_SCL=0
PIN_TGS2600=0


# update thingspeak routine (max once every 15 seconds)
def update_thingspeak(data1, data2, data3, data5):
	params = urllib.urlencode({"field1": data1, "field2": data2, "field3": data3, "field5": data5,'key':THINGSPEAK_APIWRITE})
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


def get_current_aqi():
	'''
	Returns the instantaneous AQI from the PPD42NS sensor
	'''
	s = air_quality.sensor(pi, 7) # set the GPIO pin number
	time.sleep(30) # Use 30s for a properly calibrated reading.
	g, r, c = s.read() # get the gpio, ratio and concentration in particles / 0.01 ft3
	concentration_ugm3 = s.pcs_to_ugm3(c) # convert to SI units
	aqi = s.ugm3_to_aqi(concentration_ugm3) # convert SI units to US AQI (instantaneous only)
	return aqi


# main loop
if __name__ == "__main__":

	pi = pigpio.pi()

	# Humidity and temp from DHT22 (outisde)
	s = DHT22.sensor(pi, PIN_DHT22, LED=None, power=8)   
	s.trigger()
	time.sleep(0.2)
	humidity=s.humidity()
	temp1=s.temperature()
	
	# Humidity and temp from DHT22 (inside)
	#si = DHT22.sensor(pi, PIN_DHT22i, LED=None, power=8)   
	#si.trigger()
	#time.sleep(0.2)
	#humidityi=si.humidity()
	
	# temp and pressure from BMP085
	temp2=BMP085sensor.read_temperature()
	pressure = BMP085sensor.read_pressure()

	# calc average temp of 2 sensors
	temperature = 0
	temperature=(temp1+temp2)/2
	
	# get reading from air quality sensor
	airq = get_current_aqi()
	
	try: 
		with open('aqireadings.q', 'rb') as file:
			q = pickle.load(file) # load q
	except IOError as error:
		q = deque(maxlen=4) # create q if no file exists (first run only)
	q.append(airq) # Append latest reading to start of queue
	aqi_1hour_average = sum(q)/len(q) # calculate average
	with open('aqireadings.q', 'wb') as file:
		pickle.dump(q, file) # save queue to local file

	update_thingspeak(temperature, humidity, pressure, aqi_1hour_average)
	print "Temp (DHT22) " + str(temp1)
	print "Temp (BMP) " + str(temp2)
	print "Humidity (outide): " + str(humidity)
	#print "Humidity (inside): " + str(humidityi)
	print "Pressure: " + str(pressure)
	print "AQI 1-hour average" + str(aqi_1hour_average)

	
	sys.exit()