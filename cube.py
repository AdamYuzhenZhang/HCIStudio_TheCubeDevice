import time
import board
import busio
import adafruit_mpr121
import smbus

import paho.mqtt.client as mqtt
import uuid

import mpu6050

client = mqtt.Client(str(uuid.uuid1()))
client.tls_set()
client.username_pw_set('idd', 'device@theFarm')

client.connect(
    'farlab.infosci.cornell.edu',
    port=8883)

topic = 'IDD/nek/twizzler'

i2c = busio.I2C(board.SCL, board.SDA)

mpr121 = adafruit_mpr121.MPR121(i2c)
mpu = mpu6050.mpu6050(0x68)

while True:
    for i in range(12):
        if mpr121[i].value:
        	val = f"Twizzler {i} touched!"
        	print(val)
        	#client.publish(topic, val)

    accel_data = mpu.get_accel_data()
    gyro_data = mpu.get_gyro_data()

    print("Ax:{:.4f}\tAy:{:.4f}\tAz:{:.4f}\tGx:{:.4f}\tGy:{:.4f}\tGz:{:.4f} ".format(accel_data['x'], accel_data['y'],
                                                                                     accel_data['z'], gyro_data['x'],
                                                                                     gyro_data['y'], gyro_data['z']))
    time.sleep(0.25)