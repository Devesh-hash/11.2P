import RPi.GPIO as GPIO
import time
import requests

GPIO.setwarnings(False)
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)

TRIG = 4
ECHO = 18
BUZZER = 21
GREEN = 17
YELLOW = 27
RED = 22

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(GREEN, GPIO.OUT)
GPIO.setup(YELLOW, GPIO.OUT)
GPIO.setup(RED, GPIO.OUT)
GPIO.setup(BUZZER, GPIO.OUT)

def green_light():
    GPIO.output(GREEN, GPIO.HIGH)
    GPIO.output(YELLOW, GPIO.LOW)
    GPIO.output(RED, GPIO.LOW)

def yellow_light():
    GPIO.output(GREEN, GPIO.LOW)
    GPIO.output(YELLOW, GPIO.HIGH)
    GPIO.output(RED, GPIO.LOW)

def red_light():
    GPIO.output(GREEN, GPIO.LOW)
    GPIO.output(YELLOW, GPIO.LOW)
    GPIO.output(RED, GPIO.HIGH)

def buzzer():
    GPIO.output(BUZZER, True)
    
def get_distance():
    GPIO.output(TRIG, True)
    time.sleep(0.0001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == False:
        start = time.time()

    while GPIO.input(ECHO) == True:
        end = time.time()

    sig_time = end-start

    distance = sig_time/0.000058

    print(' Distance: {} cm' .format(distance))
    return distance

while True:
    distance = get_distance()
    time.sleep(1)    
    
    if distance >= 20:
        green_light()
    elif 20 > distance > 10 :
        yellow_light()
        
        requests.post('https://maker.ifttt.com/trigger/motion_detector/with/key/max6q6ics_WzrMo_zb_Y-' ,params = {"value1" : "Warning" , "value2" : "Motion Detected" })
        time.sleep(5)   
    elif distance <= 10:
        red_light()
        
        requests.post('https://maker.ifttt.com/trigger/motion_detector/with/key/max6q6ics_WzrMo_zb_Y-' , params = {"value1" : "Alert" , "value2" : "Intruder Detected", "value3" : "Call 911"})
        time.sleep(10)
       
        