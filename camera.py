from distutils.log import error
from importlib.resources import path
from picamera import PiCamera
import os
import sys

class Camera:
    def __init__(self, path):
        self.camera = PiCamera()
        self.path = path
        try:
            os.mkdir(path)
            print("Folder ", path, "created")
        except FileExistsError:
            print("Folder", path, "already exists")
        print("Camera initalised")

    def capture(self, imageName):
        try:
            print("Starting Capture...")
            self.camera.capture(self.path + imageName)
            print("Capture success")
        except error:
            print("Capture failed with error: ", error)
