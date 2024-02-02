import numpy as np
import random

def generate_microscope_image(parasite_area=0.25, image_size=100):

    parasite_radius = int(np.sqrt(parasite_area * image_size * image_size / np.pi))
    # Generate a circular parasite
    center_x, center_y = random.randint(parasite_radius, image_size-parasite_radius-1), random.randint(parasite_radius, image_size-parasite_radius-1)

    return (center_x, center_y, parasite_radius)

def generate_dye_sensor_image(dye_area=0.1, image_size=100):
    total_size = image_size * image_size
    dye_size = int(dye_area * total_size)

    # Generate a random position for the top-left corner of the rectangle
    x_start, y_start = random.randint(0, image_size-1), random.randint(0, image_size-1)

    # Calculate the width and height of the rectangle
    width = int((dye_size / total_size) * image_size)
    height = dye_size // width

    # Ensure the rectangle stays within the image boundaries
    if x_start + width >= image_size:
        width = image_size - x_start - 1
    if y_start + height >= image_size:
        height = image_size - y_start - 1

    return (x_start, x_start + width, y_start, y_start + height)

