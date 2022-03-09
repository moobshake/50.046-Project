import climage, os



def display(image_name):
    image_folder = os.path.abspath("images")
    output = climage.convert(os.path.join(image_folder, image_name), is_unicode=True, is_256color=True)
    print(output)



display("mario.jpg")