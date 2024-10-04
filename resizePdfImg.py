from PIL import Image
import os
import concurrent.futures

# Define the path to the folder with your images
input_folder = "pdf_imgs"
output_folder = "re_imgs"

if os.path.exists(output_folder):
    # cleaning the output folder
    for f in os.listdir(output_folder):
        os.remove(os.path.join(output_folder, f))
        
# Ensure the output folder exists
if not os.path.exists(output_folder):
    os.makedirs(output_folder)


# Define the desired size
target_size = (640, 640)

def resize_image(filename):
    if filename.endswith((".jpg", ".jpeg", ".png", ".bmp")):  # Add more formats if needed
        img_path = os.path.join(input_folder, filename)
        img = Image.open(img_path)
        
        # Resize the image
        img_resized = img.resize(target_size, Image.LANCZOS)
        
        # Save the resized image to the output folder
        img_resized.save(os.path.join(output_folder, filename))

# Use ThreadPoolExecutor to apply threading
with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
    executor.map(resize_image, os.listdir(input_folder))

print("All images resized successfully!")
