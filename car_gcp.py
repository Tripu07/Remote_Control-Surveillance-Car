from sense_hat import SenseHat
import datetime
import time
import jwt
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)


TRIG=16
ECHO=18

#  Distance
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

GPIO.setup(7,GPIO.OUT)
GPIO.setup(11,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)
GPIO.setup(15,GPIO.OUT)

#  Motion
GPIO.setup(22,GPIO.IN)

#Sound

GPIO.setup(40,GPIO.IN)


def left():
    GPIO.output(15,True)
    GPIO.output(11,False)
    GPIO.output(7,False)
    GPIO.output(13,False)
    
GPIO.output(15,False)
GPIO.output(11,False)
GPIO.output(7,False)
GPIO.output(13,False)
    


# Define some project-based variables to be used below. This should be the only
# block of variables that you need to edit in order to run this script

ssl_private_key_filepath = '/home/pi/demo_private.pem'
ssl_algorithm = 'RS256' # Either RS256 or ES256
root_cert_filepath = '/home/pi/roots.pem'
project_id = 'practice-308413'
gcp_location = 'asia-east1'
registry_id = 'my_registry'
device_id = 'my_device'

# end of user-variables

cur_time = datetime.datetime.utcnow()

def create_jwt():
  token = {
      'iat': cur_time,
      'exp': cur_time + datetime.timedelta(minutes=60),
      'aud': project_id
  }

  with open(ssl_private_key_filepath, 'r') as f:
    private_key = f.read()

  return jwt.encode(token, private_key, ssl_algorithm)

_CLIENT_ID = 'projects/{}/locations/{}/registries/{}/devices/{}'.format(project_id, gcp_location, registry_id, device_id)
_MQTT_TOPIC = '/devices/{}/events'.format(device_id)

client = mqtt.Client(client_id=_CLIENT_ID)
# authorization is handled purely with JWT, no user/pass, so username can be whatever
client.username_pw_set(
    username='unused',
    password=create_jwt())

def error_str(rc):
    return '{}: {}'.format(rc, mqtt.error_string(rc))

def on_connect(unusued_client, unused_userdata, unused_flags, rc):
    print('on_connect', error_str(rc))

def on_publish(unused_client, unused_userdata, unused_mid):
    print('on_publish')

client.on_connect = on_connect
client.on_publish = on_publish

client.tls_set(ca_certs=root_cert_filepath) # Replace this with 3rd party cert if that was used when creating registry
client.connect('mqtt.googleapis.com', 8883)
client.loop_start()

# Could set this granularity to whatever we want based on device, monitoring needs, etc

while True:
   

    
    
    
    GPIO.output(TRIG,0)
    time.sleep(1)
    GPIO.output(TRIG,1)
    time.sleep(0.00001)
    GPIO.output(TRIG,0)

     
    

    x=GPIO.input(22)
    y=GPIO.input(40)
    
    while GPIO.input(ECHO)==0:
        pass

    pulse_start=time.time() 
    
       

    while GPIO.input(ECHO)==1:
        pass

    pulse_end=time.time()

    pulse_time=pulse_end-pulse_start
    distance=pulse_time*17150
    distance=round(distance,2)
    
    if distance<110:
        
      
        print()

        if x==1:
            
            xflag="Motion Detected"
            print(xflag)
        elif x==0:
            xflag="Motion Not Detected"
            print(xflag)
        if y==1:
            yflag="Sound Detected"
            print(yflag)
        elif y==0:
            yflag="Sound Not Detected"
            print(yflag)
        
       
        GPIO.output(15,False)
        GPIO.output(11,False)
        GPIO.output(7,False)
        GPIO.output(13,False)
        payload = f'Stopped at an object distance of {distance},{xflag},{yflag}'

  # Uncomment following line when ready to publish
        client.publish(_MQTT_TOPIC, payload, qos=1)

        print(payload)

        time.sleep(1)
        exit()
        
    elif distance>100:
        print()
        
        if x==1:
            xflag="Motion Detected"
            print(xflag)
        elif x==0:
            xflag="Motion Not Detected"
            print(xflag)
        if y==1:
            yflag="Sound Detected"
            print(yflag)
        elif y==0:
            yflag="Sound Not Detected"
            print(yflag)

        GPIO.output(15,True)
        GPIO.output(11,True)
        GPIO.output(7,False)
        GPIO.output(13,False)

        payload = f'Object distance at {distance} ,{xflag},{yflag}'

        client.publish(_MQTT_TOPIC, payload, qos=1)

        print(payload)

        
        
    
GPIO.cleanup()


client.loop_stop()
