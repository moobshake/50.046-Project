import camera, time
import awsyy, display
import boto3
from gpiozero import MotionSensor

CONST_IMAGE_PATH = "./images/"
CONST_ADVERT_PATH = "./advertisements/"
CONST_AD_BUCKET_NAME = "iot-fastgame-proj-ads"
CONST_VIEWER_BUCKET_NAME = "iot-fastgame-proj-viewers"

# Initialization for sensors
pir = MotionSensor(4)
c = camera.Camera(CONST_IMAGE_PATH)


# Upon initialisation, download all S3 images (Currently no credentials)
# awsyy.download_images(CONST_AD_BUCKET_NAME, CONST_VIEWER_BUCKET_NAME, CONST_ADVERT_PATH)

while True:
    pir.wait_for_motion()

    # Captures image
    c.capture("viewer")

    # Upload to S3 via mqtt

    # Get returned tags from S3

    # Display image
    display.display("mario.jpg", CONST_ADVERT_PATH)

    pir.wait_for_no_motion()
    print("f u wei wen")



