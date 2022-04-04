import climage, os, sys

def display(image_name, image_folder):
    output = climage.convert(os.path.join(image_folder, image_name), is_unicode=True, is_256color=True)
    print(output)
