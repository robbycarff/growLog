from Adafruit_BME280 import *
import datetime
import RPi.GPIO as GPIO
from time import sleep

#pinout from raspberry pi 3 using BCM 17,27
Relay_channel = [17, 27]
setTemp = 75

def setup():
    #setting up GPIO for turning relays on/off 
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(Relay_channel, GPIO.OUT, initial=GPIO.LOW)
    # creating global senor
    # (temp, pressure, humidity)
    global sensor
    sensor = BME280(t_mode=BME280_OSAMPLE_8, p_mode=BME280_OSAMPLE_8, h_mode=BME280_OSAMPLE_8)
    #creating global running variable
    global on
    on = True


def dateTime():
    #creating global dateTime variable
    global now
    #method to get date and time, can be called where ever (now is global)  
    now = datetime.datetime.now()
    

def firstRead():
    #getting date and time
    dateTime()
    #printing date and time
    print "Current date and time"
    print now.strftime("%Y-%m-%d %H:%M")
    
    #reading from sensor
    degrees = sensor.read_temperature_f()
    pascals = sensor.read_pressure()
    hectopascals = pascals / 100
    # printing read data
    print 'Temp      = {0:0.3f} deg F'.format(degrees)
    print 'Pressure  = {0:0.2f} hPa \n'.format(hectopascals)
    


def loop():
    # writing out to this file
    # a appends, instead of w which overwrites the entire file
    f = open('tempFolder.txt', 'a')
    #getting date and time
    dateTime()
    #writing date and time
    f.write("\nInitial date and time\n")
    f.write (now.strftime("%Y-%m-%d %H:%M") + '\n')
    
    
    
    while on:
        degrees = sensor.read_temperature_f()
        f.write('Temp = {0:0.3f} deg F \n'.format(degrees) )
        print 'Temp = {0:0.3f} deg F'.format(degrees)
        time.sleep(5)
        #change these to if statements based on the temperature read
        #for i in range(0, len(Relay_channel)):
        if (degrees > setTemp):
            print 'Temperature too high, turning on A/C'
            print '...Relay channel %d on' % 0
            GPIO.output(Relay_channel[0], GPIO.HIGH)
            sleep(0.5)
            print '...Relay channel %d off' % 1
            GPIO.output(Relay_channel[1], GPIO.LOW)
            sleep(0.5)
            
        else:
            print 'Temperature too high, turning on HEAT'
            print '...Relay channel %d off' % 0
            GPIO.output(Relay_channel[0], GPIO.LOW)
            sleep(0.5)
            print '...Relay channel %d on' % 1
            GPIO.output(Relay_channel[1], GPIO.HIGH)
            sleep(0.5)
        
    f.close()

def destroy():
    GPIO.output(Relay_channel, GPIO.LOW)
    on = False
    
    
    
if __name__ == "__main__": #this is where the program starts
    setup() #runs the setup method
    try:
        firstRead() # initial data read
        loop() #runs our loop method 
    except KeyboardInterrupt:
        destroy() #runs our destroy method when ctrl+c is pushed