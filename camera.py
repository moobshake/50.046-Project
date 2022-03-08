from distutils.log import error
from importlib.resources import path
from picamera import PiCamera
import os
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

class Camera:
    def __init__(self, path):
        logging.info("Camera initialising...")
        self.camera = PiCamera()
        self.path = path
        try:
            os.mkdir(path)
            logging.info("Folder ", path, "created")
        except FileExistsError:
            logging.info("Folder", path, "already exists")
        logging.info("Camera initalised")

    def capture(self, imageName):
        try:
            logging.info("Starting Capture...")
            self.camera.capture(self.path + "/" + imageName + ".png")
            logging.info("Capture success")
        except error:
            logging.error("Capture failed with error: ", error)
