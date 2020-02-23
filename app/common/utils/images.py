from PIL import Image


def resize_image(image_path, height, width):
    img = Image.open(image_path)

    if img.height > height or img.width > height:
        output_size = (height, width)
        img.thumbnail(output_size)
        img.save(image_path)
