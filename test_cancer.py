import numpy as np
import random


def overlap_area(C_x, C_y, r, x_start, x_end, y_start, y_end):
    # Calculate the closest point on the rectangle to the circle
    closest_x = max(x_start, min(C_x, x_end))
    closest_y = max(y_start, min(C_y, y_end))
    
    # Check if the closest point is inside the circle
    if (closest_x - C_x)**2 + (closest_y - C_y)**2 > r**2:
        return 0  # No overlap
    
    # Check if the circle center is inside the rectangle
    if x_start <= C_x <= x_end and y_start <= C_y <= y_end:
        return min(x_end - x_start, y_end - y_start)  # Circle is completely inside the rectangle
    
    # Calculate the area of overlap using geometric techniques
    dx = min(abs(x_start - C_x), abs(x_end - C_x))
    dy = min(abs(y_start - C_y), abs(y_end - C_y))
    
    return max(0, (r**2 * (3.14159265358979323846 / 4) - dx * dy))


def has_cancer_optimized(microscope_image, dye_sensor_image, cancer_threshold=0.1):

    # Unpack values from the single tuple
    x_start, x_end, y_start, y_end = dye_sensor_image
    center_x, center_y, parasite_radius = microscope_image
    overlapped_area =  overlap_area(center_x, center_y, parasite_radius, x_start, x_end, y_start, y_end)

    area_parasite = (parasite_radius**2 * (3.14159265358979323846 / 4))
    # Calculate the percentage of cancer cells in the overlapped region
    overlap_percentage = overlapped_area / area_parasite

    # Check if the overlap percentage exceeds the cancer threshold
    print("overlapped " , overlap_percentage)
    return overlap_percentage > cancer_threshold


def has_cancer(microscope_image, dye_sensor_image, cancer_threshold=0.1):
    parasite_area = np.sum(microscope_image)
    dye_area = len(dye_sensor_image)
    cancer_percentage = dye_area / parasite_area
    return cancer_percentage > cancer_threshold
