import camera, time
import subprocess
import awsyy
import display
import boto3
from gpiozero import MotionSensor

CONST_IMAGE_PATH = "./images/"
CONST_ADVERT_PATH = "./advertisements/"
CONST_AD_BUCKET_NAME = "iot-fastgame-proj-ads"
CONST_VIEWER_BUCKET_NAME = "iot-fastgame-proj-viewers"
CONST_CAMERA_CAPTURE = "capture.png"
CONST_STANDBY_IMAGE = "black.png"

# Initialization for sensors
print("Initialising PIR sensor & Camera...")
pir = MotionSensor(4)
c = camera.Camera(CONST_IMAGE_PATH)
print("PIR & Camera online")


# Upon initialisation, download all S3 images (Currently no credentials)
print("Initialising Advert folder. Contacting S3...")
# awsyy.download_images(CONST_AD_BUCKET_NAME, CONST_VIEWER_BUCKET_NAME, CONST_ADVERT_PATH)
print("Local copy of advertisments created")

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

