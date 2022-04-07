import subprocess

# per image display
def display(image_folder, image_name):
    return subprocess.Popen(["feh", "--hide-pointer", "-x", "-f" , "-q", "-B", "black", "-g", "-fullscreen", "-y", "1280x800", image_folder + image_name])

# slideshow image display
def display_images(image_folder):
    return subprocess.Popen(["feh", "--hide-pointer", "-x", "-f" , "-q", "-B", "black", "-g", "-fullscreen", "-y", "1280x800", image_folder])
