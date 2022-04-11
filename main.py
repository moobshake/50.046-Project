from numpy import False_
import camera
import subprocess
import awsyy
import display
import boto3
from gpiozero import MotionSensor
from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
import time as t
import json
import ast
from decimal import Decimal
import os

# Define important paths #############################################################################################
CONST_IMAGE_PATH = "./images/"
CONST_ADVERT_PATH = "./advertisements/"
CONST_AD_BUCKET_NAME = "cciot-fastgame-proj-ads"
CONST_VIEWER_BUCKET_NAME = "cciot-fastgame-proj-viewers"
CONST_CAMERA_CAPTURE = "capture.png"
CONST_STANDBY_IMAGE = "black.png"
CONST_IMAGE_DISPLAY_FILE = "imgstodisplay.txt"
########################################################################################################################

# Define ENDPOINT, CLIENT_ID, PATH_TO_CERTIFICATE, PATH_TO_PRIVATE_KEY, PATH_TO_AMAZON_ROOT_CA_1, MESSAGE, TOPIC, and RANGE
ENDPOINT = "a2pxoxfco87kve-ats.iot.ap-southeast-1.amazonaws.com"
CLIENT_ID = "cciot-proj-rpi"
PATH_TO_CERTIFICATE = "./certs/cciot-proj-rpi.cert.pem"
PATH_TO_PRIVATE_KEY = "./certs/cciot-proj-rpi.private.key"
PATH_TO_AMAZON_ROOT_CA_1 = "./certs/root-CA.crt"
VIEWERDEMOS_TOPIC = "cciot-fastgame/viewerdemos"
ADSUPLOAD_TOPIC = "cciot-fastgame/aduploads"
########################################################################################################################

####
GLOBAL_TIMEOUT = False
####
# DynamoDB #####################################################################################################
def put_viewcount(filename, dynamodb=None):
    if not dynamodb:
         dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('viewerCount_byAds')
    response = table.update_item(
        Key={
            'advertisement-name': filename
        },
        UpdateExpression="set viewCount = viewCount + :val",
        ExpressionAttributeValues={
            ':val': 1
        },
        ReturnValues="UPDATED_NEW"
    )
    return response
########################################################################################################################

# Callback when the subscribed topic receives a message ###############################################################
def on_message_received_viewerdemos(topic, payload, dup, qos, retain, **kwargs):
    print("Got tags from S3 based on Reckognition")
    print("Received message from topic '{}': {}".format(topic, payload.decode()))
    viewerDemos_list = ast.literal_eval(payload.decode())
    print(viewerDemos_list)
    f = open("tags.json") 
    adtags = json.load(f)
    with open(CONST_IMAGE_DISPLAY_FILE, "w") as outfile:
        if "Default" in viewerDemos_list:
                outfile.write("mcdonalds.png" + "\n")
        else:
            for ad in adtags:
                inside = False
                for tag in ad["tags"]:
                    if tag in viewerDemos_list:
                        inside = True
                if inside:
                    outfile.write(ad["name"] + "\n")
    global GLOBAL_TIMEOUT 
    GLOBAL_TIMEOUT = False

# Callback when the subscribed topic receives a message ###############################################################
def on_message_received_adsupload(topic, payload, dup, qos, retain, **kwargs):
    print("Received message from topic '{}': {}".format(topic, payload.decode()))
    payload_string = payload.decode()
    awsyy.download_image(CONST_AD_BUCKET_NAME, CONST_ADVERT_PATH, payload_string)
########################################################################################################################

# Initialization for sensors ###############################################################
print("Initialising PIR sensor & Camera...")
pir = MotionSensor(4)
c = camera.Camera(CONST_IMAGE_PATH)
print("PIR & Camera online")
########################################################################################################################

# Upon initialisation, download all S3 images (Currently no credentials) ########################################
print("Initialising Advert folder. Contacting S3...")
awsyy.download_images(CONST_AD_BUCKET_NAME, CONST_ADVERT_PATH)
print("Local copy of advertisments created")
########################################################################################################################

# Spin up resources ###############################################################
event_loop_group = io.EventLoopGroup(1)
host_resolver = io.DefaultHostResolver(event_loop_group)
client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)
mqtt_connection = mqtt_connection_builder.mtls_from_path(
            endpoint=ENDPOINT,
            cert_filepath=PATH_TO_CERTIFICATE,
            pri_key_filepath=PATH_TO_PRIVATE_KEY,
            client_bootstrap=client_bootstrap,
            ca_filepath=PATH_TO_AMAZON_ROOT_CA_1,
            client_id=CLIENT_ID,
            clean_session=False,
            keep_alive_secs=6
        )
print("Connecting to {} with client ID '{}'...".format(
        ENDPOINT, CLIENT_ID))
# Make the connect() call
connect_future = mqtt_connection.connect()
# Future.result() waits until a result is available
connect_future.result()
print("Connected!")

# Subscribe ###############################################################
print("Subscribing to topic '{}'...".format(VIEWERDEMOS_TOPIC))
subscribe_future, packet_id = mqtt_connection.subscribe(
    topic=VIEWERDEMOS_TOPIC,
    qos=mqtt.QoS.AT_LEAST_ONCE,
    callback=on_message_received_viewerdemos)
########################################################################################################################

# Subscribe ###############################################################
print("Subscribing to topic '{}'...".format(ADSUPLOAD_TOPIC))
subscribe_future, packet_id = mqtt_connection.subscribe(
    topic=ADSUPLOAD_TOPIC,
    qos=mqtt.QoS.AT_LEAST_ONCE,
    callback=on_message_received_adsupload)
########################################################################################################################

# Publish for view count ###############################################################
mqttclient = boto3.client('iot-data')
########################################################################################################################

# Start of SUPERLOOP ###############################################################
image = display.display(CONST_IMAGE_PATH, CONST_STANDBY_IMAGE)

while True:
    print("Waiting for viewer to be sensed")
    pir.wait_for_motion()
    image.kill()
    print("Viewer detected!")

    # Captures image
    c.capture(CONST_CAMERA_CAPTURE)

    # Upload to S3 via mqtt
    print("Contacting S3 via MQTT to upload viewer image")
    awsyy.upload_images(CONST_VIEWER_BUCKET_NAME, CONST_IMAGE_PATH, CONST_CAMERA_CAPTURE)
    GLOBAL_TIMEOUT = True
    # time wait for viewer demo
    t.sleep(5)
    if GLOBAL_TIMEOUT:
        image = display.display(CONST_ADVERT_PATH, "mcdonalds.png")
        put_viewcount("mcdonalds.png")
        t.sleep(5)
        image.kill()
        GLOBAL_TIMOUT = False
    else:
        f = open(CONST_IMAGE_DISPLAY_FILE, "r")
        
        print("Displaying advertisement...")

        advert_name = f.readlines()
        # Display the image
        for i in advert_name:
            if i != "": 
                i = i.strip("\n")
                image = display.display(CONST_ADVERT_PATH, i)
                put_viewcount(i)
                t.sleep(5)
                image.kill()
                # image = display.display(CONST_IMAGE_PATH, CONST_CAMERA_CAPTURE)
 
    pir.wait_for_no_motion()
    # if no motion, then kill the image
    image.kill()
    image = display.display(CONST_IMAGE_PATH, CONST_STANDBY_IMAGE)
    print("User left, display will go into standby to save power...")
########################################################################################################################
