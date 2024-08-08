import RPi.GPIO as gpio
import time
import context  # Ensures paho is in PYTHONPATH
import paho.mqtt.client as mqtt

trig = 5
echo = 6
print("start")
gpio.setmode(gpio.BCM)
gpio.setup(trig, gpio.OUT)
gpio.setup(echo, gpio.IN)
pulse_start = time.time()
distance = None
def back_distance():
   try :
      while True :
         global distance
         gpio.output(trig, False)
         time.sleep(0.1) 
         gpio.output(trig, True)
         time.sleep(0.00002)
         gpio.output(trig, False)      
         while gpio.input(echo) == 0 :
            pulse_start = time.time()
         while gpio.input(echo) == 1 :
            pulse_end = time.time()

         pulse_duration = pulse_end - pulse_start
         distance_1 = pulse_duration * 17000
         distance_2 = round(distance_1, 0)
        
         if distance_2 <= 30:
            distance = False
         else:
            distance = True

         print("Distance : ", distance_2, "cm, T or F = ", distance)
        
         break
   except:
      gpio.cleanup()
      
def on_connect(client, mosq, obj, rc):
   print("on_connet:: Connected with result code "+str(rc))
   print("rc: " + str(rc))

def on_message(mosq, obj, msg):
   topic = msg.topic
   payload = msg.payload.decode("utf-8")
   a = topic + payload

def on_publish(mosq, obj, mid):
   print("mid: " + str(mid), "obj : ", distance)

def on_log(mosq, obj, level, string):
   print(string)
   
RST = 24
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

client = mqtt.Client()
client.on_message = on_message
client.on_connect = on_connect
client.on_publish = on_publish

client.on_log = on_log

client.connect('localhost', 1883, 60)

client.loop_start()

run = True
try:
   while run:
      back_distance()
      client.publish("back_distance", distance)
      print("publish complete")
      pass
except KeyboardInterrupt:
   print("exiting..")
client.loop_stop()

