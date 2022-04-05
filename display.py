import subprocess

def display(image_folder, image_name):
    return subprocess.Popen(["feh", "--hide-pointer", "-x", "-q", "-B", "black", "-g", "-fullscreen", "-y", "1280x800", image_folder + image_name])
