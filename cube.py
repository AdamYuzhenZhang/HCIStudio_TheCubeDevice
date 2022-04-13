import math
import time
import board
import busio
import adafruit_mpr121
import smbus

import paho.mqtt.client as mqtt
import uuid

import mpu6050
import qwiic_button

client = mqtt.Client(str(uuid.uuid1()))
client.tls_set()
client.username_pw_set('idd', 'device@theFarm')

client.connect(
    'farlab.infosci.cornell.edu',
    port=8883)

topic = 'IDD/HCI'

i2c = busio.I2C(board.SCL, board.SDA)

mpr121 = adafruit_mpr121.MPR121(i2c)
mpr121.begin()
mpu = mpu6050.mpu6050(0x68)
# Setup button
button = qwiic_button.QwiicButton()
button.begin()

while True:
    mpr_string = ""
    mpu_string = ""

    if button.is_button_pressed():
        mpr121 = adafruit_mpr121.MPR121(i2c)
        mpr121.begin()

    for i in range(12):
        if mpr121[i].value:
        	mpr_string += "1 "
        else:
            mpr_string += "0 "
    print("MPR string: " + mpr_string)

    accel_data = mpu.get_accel_data()
    gyro_data = mpu.get_gyro_data()

    AcX, AcY, AcZ = accel_data['x'], accel_data['y'], accel_data['z']

    # pitch
    xAng = math.atan2(AcZ,AcX)*180/math.pi
    # roll
    yAng = math.atan2(AcZ,AcY)*180/math.pi
    # yaw
    zAng = math.atan2(math.sqrt(AcY*AcY+AcZ*AcZ),AcX)*180/math.pi

    mpu_string = "{:.4f} {:.4f} {:.4f}".format(xAng, yAng, zAng)

    #print("Xangle:{:.4f}\tYangle:{:.4f}\tZangle:{:.4f} ".format(xAng, yAng, zAng))
    print("MPU string: " + mpu_string)
    #print("Ax:{:.4f}\tAy:{:.4f}\tAz:{:.4f}\tGx:{:.4f}\tGy:{:.4f}\tGz:{:.4f} ".format(accel_data['x'], accel_data['y'],
    #                                                                                 accel_data['z'], gyro_data['x'],
    #                                                                                 gyro_data['y'], gyro_data['z']))

    val = mpr_string + mpu_string
    client.publish(topic, val)
    time.sleep(0.5)