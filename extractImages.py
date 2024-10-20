import os
import subprocess
import shutil
from time import time

def extract_images_using_pdftohtml(pdf_path, output_folder):
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Extract images using pdftohtml
    for pdf_file in os.listdir(pdf_path):
        if pdf_file.endswith(".pdf") or pdf_file.endswith(".PDF"):
            full_pdf_path = os.path.join(pdf_path, pdf_file)
            # Create a temporary folder to extract images for each PDF
            temp_folder = os.path.join(output_folder, f'{pdf_file.split(".")[0]}{int(time())}')
            if not os.path.exists(temp_folder):
                os.makedirs(temp_folder)

            # Run the pdftohtml command to extract images into the temp folder
            subprocess.run(["pdftohtml", "-c", "-hidden", "-nodrm", "-fmt", "jpeg", full_pdf_path, temp_folder])
            
            # Rename and move images from temp folder to the output folder
            rename_and_move_images(pdf_file, temp_folder, output_folder)
            
            # Clean up the temp folder
            shutil.rmtree(temp_folder)
    
    print(f"Images extracted to {output_folder}")

def rename_and_move_images(pdf_file, temp_folder, output_folder):
    # Get list of images
    image_files = [f for f in os.listdir(temp_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg'))]
    
    total_images = len(image_files)
    base_pdf_name = os.path.splitext(pdf_file)[0]  # Get PDF file name without extension
    
    for i, image_file in enumerate(sorted(image_files), 1):  # Sort to ensure consistent ordering
        # Get the current time
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        new_name = f"{base_pdf_name}_image{i}_of_{total_images}_{current_time}{os.path.splitext(image_file)[1]}"  # Preserve the image extension
        old_image_path = os.path.join(temp_folder, image_file)
        new_image_path = os.path.join(output_folder, new_name)
        shutil.move(old_image_path, new_image_path)

def clean_output_folder(output_folder):
    # Remove all non-image files from the output folder
    allowed_extensions = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".svg"}
    
    for filename in os.listdir(output_folder):
        file_path = os.path.join(output_folder, filename)
        # Check file extension
        if not any(filename.lower().endswith(ext) for ext in allowed_extensions):
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)  # Remove directories if any exist
            except Exception as e:
                print(f"Error deleting file {file_path}: {e}")

# Example usage
pdf_path = "pdfs"
output_folder = "pdf_imgs/"

# Step 1: Clear the output folder
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
for f in os.listdir(output_folder):
    os.remove(os.path.join(output_folder, f))

# Step 2: Extract images using pdftohtml
extract_images_using_pdftohtml(pdf_path, output_folder)

# Step 3: Clean the output folder and remove non-image files
clean_output_folder(output_folder)

# Step 4: Resize images using the existing resize script
print("Resizing images...")
subprocess.run(["python", "resizePdfImg.py"])
