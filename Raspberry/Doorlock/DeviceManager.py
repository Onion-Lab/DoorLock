import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT)
GPIO.setup(16,GPIO.OUT)
GPIO.output(16,True)

def doorOpen():
    GPIO.output(17,False)
    time.sleep(0.3)
    GPIO.output(17,True)

def ledOn():
    GPIO.output(16,True)

def ledOff():
    GPIO.output(16,False)