from generate_images import generate_dye_sensor_image, generate_microscope_image
from test_cancer import has_cancer_optimized
import numpy as np
from PIL import Image, ImageEnhance
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import os
import time
import tracemalloc



class MicrobiologyResearchRunner:
    def __init__(self):
        self.microscope_images = []
        self.dye_sensor_images = []
        self.blended_images = []
    
    def show_microscope_image(self, image):
        plt.imshow(image, cmap='plasma_r')
        plt.title("Parasite")
        plt.show()
    
    def show_image(self, image):
        red_to_blue_cmap = LinearSegmentedColormap.from_list('RedToBlue', ['red', 'white', 'blue'])
        plt.imshow(image, cmap='Oranges_r')
        plt.title("Parasite and Dye Overlapped")
        plt.show()
    
    def save_image(self, image, save_path="Cancer_Images", filename="overlapped_image", title = "Parasite Image"):
        plt.imshow(image, cmap='Oranges_r')
        plt.title(title)
        plt.axis('off')  # Turn off axis labels and ticks
        plt.savefig(os.path.join(save_path, filename), bbox_inches='tight', pad_inches=0)
        plt.close()  # Close the current figure to avoid memory issues


    def create_circle_image(self, microscope_image, image_size):

        C_x, C_y, radius = microscope_image
        # Create a NumPy array for the image
        image_array = np.zeros((image_size, image_size), dtype=np.uint8)

        # Generate grid coordinates
        x, y = np.meshgrid(np.arange(image_size), np.arange(image_size))

        # Calculate distance from each pixel to the circle center
        distance = np.sqrt((x - C_x)**2 + (y - C_y)**2)

        # Set pixels inside the circle to white (255)
        image_array[distance <= radius] = 255

        # Convert the NumPy array to a PIL Image
        image = Image.fromarray(image_array,  mode='L')

        return image
    
    def create_rectangle_image(self, dye_sensor_image, image_size):
        x_start, x_end, y_start, y_end =  dye_sensor_image   

        # Create a NumPy array for the image
        image_array = np.zeros((image_size, image_size), dtype=np.uint8)

        # Generate grid coordinates
        x, y = np.meshgrid(np.arange(image_size), np.arange(image_size))

        # Set pixels inside the rectangle to white (255)
        inside_rectangle = (x >= x_start) & (x <= x_end) & (y >= y_start) & (y <= y_end)
        image_array[inside_rectangle] = 255

        # Convert the NumPy array to a PIL Image
        image = Image.fromarray(image_array,   mode='L')

        return image

    def generate_fake_data(self, num_samples=100, image_size = 500):
        for _ in range(num_samples):
            microscope_image = generate_microscope_image(0.25, image_size)
            dye_sensor_image = generate_dye_sensor_image(0.3, image_size)

            # Convert to Pillow images
            microscope_pillow_image = self.create_circle_image(microscope_image, image_size)
            dye_pillow_image = self.create_rectangle_image(dye_sensor_image, image_size)

            # Blend the images using transparency
            blended_image = Image.blend(microscope_pillow_image, dye_pillow_image, alpha=0.5)

            # Show the overlapped image
            self.show_image(blended_image)

            self.microscope_images.append(microscope_image)
            self.dye_sensor_images.append(dye_sensor_image)
            self.blended_images.append(blended_image)

            
        
        for _ in range(3):
            microscope_image = generate_microscope_image(0.25, image_size)
            # Ensure some parasites have cancer by generating dye sensor images accordingly
            dye_sensor_image = generate_dye_sensor_image(0.30, image_size)

            # Convert to Pillow images
            microscope_pillow_image = self.create_circle_image(microscope_image, image_size)
            dye_pillow_image = self.create_rectangle_image(dye_sensor_image, image_size)

            # Blend the images using transparency
            blended_image = Image.blend(microscope_pillow_image, dye_pillow_image, alpha=0.5)

            # Show the overlapped image
            self.show_image(blended_image)

            self.microscope_images.append(microscope_image)
            self.dye_sensor_images.append(dye_sensor_image)
            self.blended_images.append(blended_image)

    

    def run_cancer_detection(self):
        for i, (microscope_image, dye_sensor_image) in enumerate(zip(self.microscope_images, self.dye_sensor_images), start=1):
            has_cancer_optimized_result = has_cancer_optimized(microscope_image, dye_sensor_image)
            print(f"Parasite {i}: Microscope Image: {np.sum(microscope_image)}, Dye Sensor Image: {len(dye_sensor_image)}, Has Cancer: {has_cancer_optimized_result}")

    def run_cancer_detection(self, save_path="Cancer_Images", image_size = 500):
        
        for i, (microscope_image, dye_sensor_image, blended_image) in enumerate(zip(self.microscope_images, self.dye_sensor_images, self.blended_images), start=1):
            has_cancer_optimized_result = has_cancer_optimized(microscope_image, dye_sensor_image)
            print(f"Parasite {i} Has Cancer: {has_cancer_optimized_result}")

            if has_cancer_optimized_result:
                # Save the microscope image
                self.save_image(blended_image, save_path, f"Parasite{i}Blended_Cancer_Image", "Parasite and Dye")

                # Save the dye sensor image
                self.save_image(self.create_rectangle_image(dye_sensor_image, image_size), save_path, f"Parasite{i}Dye_Image", "Dye")
                self.save_image(self.create_circle_image(microscope_image, image_size), save_path, f"Parasite{i}Microscope_Image", "Parasite")

if __name__ == "__main__":

    start_time = time.time()
    tracemalloc.start()
    microbiology_runner = MicrobiologyResearchRunner()
    microbiology_runner.generate_fake_data(3, 1000)
    microbiology_runner.run_cancer_detection("Cancer_Images", 1000)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time} seconds")

    current, peak = tracemalloc.get_traced_memory()
    print(f"Current memory usage: {current / 10**6} MB")
    print(f"Peak memory usage: {peak / 10**6} MB")
    tracemalloc.stop()  # Stop tracing memory
