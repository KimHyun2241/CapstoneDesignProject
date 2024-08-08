import context
import paho.mqtt.client as mqtt, os
import RPi.GPIO as GPIO          
import time

# fm = front_distance, bd= back_distance
fd, bd = None, None
# hand gesture
come, away, spin, stop = None, None, None, None

hand_detect = None

# left wheel
left_en = 17
left1 = 27
left2 = 22

# right wheel
right1 = 23
right2 = 24
right_en = 25

# left wheel
GPIO.setmode(GPIO.BCM)
GPIO.setup(left1,GPIO.OUT)
GPIO.setup(left2,GPIO.OUT)
GPIO.setup(left_en,GPIO.OUT)
GPIO.output(left1,GPIO.LOW)
GPIO.output(left2,GPIO.LOW)
pl=GPIO.PWM(left_en,1000)

# right wheel
GPIO.setup(right1,GPIO.OUT)
GPIO.setup(right2,GPIO.OUT)
GPIO.setup(right_en,GPIO.OUT)
GPIO.output(right1,GPIO.LOW)
GPIO.output(right2,GPIO.LOW)
pr=GPIO.PWM(right_en,1000)

pl.start(40)
pr.start(45)

def on_connect(client, mosq, obj, rc):
   print("on_connet:: Connected with result code "+str(rc))
   print("rc: " + str(rc))

def on_message(mosq, obj, msg):
   global fd, bd, come, away, spin
   topic = msg.topic
   payload = msg.payload.decode("utf-8")
   rm = topic + payload
   print("rm : ", rm)
   print(msg.topic + " " +str(msg.qos) + " " + str(msg.payload))

   # front_distance
   if rm == "front_distanceTrue":
      #print("fd True")
      fd = True
   elif rm == "front_distanceFalse":
      #print("fd False")
      fd = False
   # back_distance
   elif rm == "back_distanceTrue":
      #print("bd True")
      bd = True
   elif rm == "back_distanceFalse":
      #print("fd False")
      bd = False
   # hand gesture
   elif rm == "hand_gestureCome":
      #print("gestureCome")
      away = False
      come = True
   elif rm == "hand_gestureAway":
      #print("gestureAway")
      come = False
      away = True
      
   elif rm == "hand_gestureSpin":
      #print("gestureStop")
      spin = True

   elif rm == "hand_gestureStop":
      #print("gestureStop")
      come = False
      away = False
   print("fd :" , fd , ", bd :" , bd , ", come :" , come , ", away :" , away, " spin :", spin, " stop :", stop)
      
def on_publish(mosq, obj, mid):
   print("mid: " + str(mid))

def on_subscribe(mosq, obj, mid, granted_qos):
   print("This means broker has acknowledged my subscribe request:")
   print("Subscribed mosq : ",mosq,"obj : ", obj,"mid : ", mid,"granted_qos : ", granted_qos)

def on_log(mosq, obj, level, string):
   print(string)
    
def separator():
   global hand_detect, fd, bd, come, away, spin, stop
   if spin == True:
      motor_stop()
      spin_motor()
      spin = False
      
   elif come == False and away == False:
      motor_stop()
      
   elif fd == True and come == True:
      come_motor()

   elif fd == False and come == True:
      motor_stop()
      
      pass
   elif fd == False and away == True:
      away_motor()
       
   elif bd == True and away == True:
      away_motor()
      
   elif bd == False and away == True:
      motor_stop()
      
      pass
   elif bd == False and come == True:
      come_motor()

def motor_controler(msg):
   move_motor = True
   stop_motor = False
   print("hand_detect",msg)
   print("motor_controler msg :", msg)
   print("motor_controler :", stop_motor, " || ", move_motor)
   if msg == "come_stop":
      print("publish come_stop")
      client.publish("come_motor", stop_motor)
   elif msg == "away_stop":
      print("publish away_stop")
      client.publish("away_motor", stop_motor)
   elif msg == "come":
      print("publish come")
      client.publish("come_motor", move_motor)
   elif msg == "away":
      print("publish away")
      client.publish("away_motor", move_motor)
   elif msg == "error":
      print("sensor error!!")
      client.publish("come_motor", stop_motor)
      client.publish("away_motor", stop_motor)

def spin_motor():
   while True:
      spin_motor()
      break

def come_motor():
   GPIO.output(left1,GPIO.LOW)
   GPIO.output(left2,GPIO.HIGH)
   GPIO.output(right1,GPIO.LOW)
   GPIO.output(right2,GPIO.HIGH)

def away_motor():
   GPIO.output(left1,GPIO.HIGH)
   GPIO.output(left2,GPIO.LOW)
   GPIO.output(right1,GPIO.HIGH)
   GPIO.output(right2,GPIO.LOW)
   
def motor_stop():
   global come, away
   GPIO.output(left1,GPIO.LOW)
   GPIO.output(left2,GPIO.LOW)
   GPIO.output(right1,GPIO.LOW)
   GPIO.output(right2,GPIO.LOW)
   come, away = False, False
      
def spin_motor():
   GPIO.output(left1,GPIO.LOW)
   GPIO.output(left2,GPIO.HIGH)
   GPIO.output(right1,GPIO.HIGH)
   GPIO.output(right2,GPIO.LOW)
   time.sleep(2.2)
   motor_stop()

RST = 24
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

client = mqtt.Client()
client.on_message = on_message
client.on_connect = on_connect
client.on_publish = on_publish
client.on_subscribe = on_subscribe
client.on_log = on_log

client.connect('localhost', 1883, 60)

client.loop_start()
client.subscribe("front_distance", 0)
client.subscribe("back_distance", 0)
client.subscribe("hand_gesture", 0)
run = True
try:
   while run:
      separator()
      time.sleep(1)
      pass
except KeyboardInterrupt:
   print("exiting..")
client.loop_stop()
