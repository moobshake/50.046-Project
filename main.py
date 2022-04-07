import camera, time
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

CONST_IMAGE_PATH = "./images/"
CONST_ADVERT_PATH = "./advertisements/"
CONST_AD_BUCKET_NAME = "iot-fastgame-proj-ads"
CONST_VIEWER_BUCKET_NAME = "iot-fastgame-proj-viewers"
CONST_CAMERA_CAPTURE = "capture.png"
CONST_STANDBY_IMAGE = "black.png"

# Define ENDPOINT, CLIENT_ID, PATH_TO_CERTIFICATE, PATH_TO_PRIVATE_KEY, PATH_TO_AMAZON_ROOT_CA_1, MESSAGE, TOPIC, and RANGE
ENDPOINT = "azwea5zu3qfbc-ats.iot.ap-southeast-1.amazonaws.com"
CLIENT_ID = "iot-fastgame-rpi"
PATH_TO_CERTIFICATE = "./certs/iot-fastgame-rpi.cert.pem"
PATH_TO_PRIVATE_KEY = "./certs/iot-fastgame-rpi.private.key"
PATH_TO_AMAZON_ROOT_CA_1 = "./certs/root-CA.crt"
VIEWERDEMOS_TOPIC = "iot-fastgame/viewerdemos"
ADSUPLOAD_TOPIC = "iot-fastgame/aduploads"
########################################################################################################################

# Callback when the subscribed topic receives a message ###############################################################
def on_message_received_viewerdemos(topic, payload, dup, qos, retain, **kwargs):
    print("Received message from topic '{}': {}".format(topic, payload.decode()))
    viewerDemos_list = ast.literal_eval(payload.decode())
    f = open("tags.json") 
    filtercheck = json.load(f)
    with open("imgstodisplay.txt", "w") as outfile:
        for i in filtercheck:
            for tag in i["tags"]:
                if tag in viewerDemos_list:
                    outfile.write(i["name"] +"\n")

# Callback when the subscribed topic receives a message ###############################################################
def on_message_received_adsupload(topic, payload, dup, qos, retain, **kwargs):
    print("Received message from topic '{}': {}".format(topic, payload.decode()))
    payload_string = payload.decode()[1:-1]
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

    # Get returned tags from S3
    print("Got tags from S3 based on Reckognition")

    print("Displaying advertisement...")
    # Display the image
    # image = display.display(CONST_ADVERT_PATH, advert_name)
    image = display.display(CONST_IMAGE_PATH, CONST_CAMERA_CAPTURE)
 
    pir.wait_for_no_motion()
    # if no motion, then kill the image
    image.kill()
    image = display.display(CONST_IMAGE_PATH, CONST_STANDBY_IMAGE)
    print("User left, display will go into standby to save power...")

