import time
import board
import busio

import paho.mqtt.client as mqtt
import uuid

import qwiic

client = mqtt.Client(str(uuid.uuid1()))
client.tls_set()
client.username_pw_set('idd', 'device@theFarm')

client.connect(
    'farlab.infosci.cornell.edu',
    port=8883)

topic = 'IDD/Spec'

#i2c = busio.I2C(board.SCL, board.SDA)

ToF = qwiic.QwiicVL53L1X()
if (ToF.sensor_init() == None):					 # Begin returns 0 on a good init
	print("Sensor online!\n")

while True:
    try:
        ToF.start_ranging()  # Write configuration bytes to initiate measurement
        time.sleep(.005)
        distance = ToF.get_distance()  # Get the result of the measurement from the sensor
        time.sleep(.005)
        ToF.stop_ranging()

        #distanceInches = distance / 25.4
        #distanceFeet = distanceInches / 12.0

        #print("Distance(mm): %s Distance(ft): %s" % (distance, distanceFeet))
        val = "{:.4f}".format(distance)
        client.publish(topic, val)
        time.sleep(0.05)

    except Exception as e:
        print(e)
