import subprocess

# per image display
def display(image_folder, image_name):
    return subprocess.Popen(["feh", "-F", "--zoom", "max", image_folder + image_name])
    # , "--hide-pointer", "-x", "-q", "-B", "black", "-g", "-fullscreen", "-f" "-y", "1280x800",

# slideshow image display
def display_images(image_folder):
    return subprocess.Popen(["feh", "--hide-pointer", "-x", "-f" , "-q", "-B", "black", "-g", "-fullscreen", "-y", "1280x800", image_folder])
