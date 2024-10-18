import fitz  # PyMuPDF
import os
import subprocess
from PIL import Image

def correct_orientation(image_path):
    # Open the image
    with Image.open(image_path) as img:
        # Manually rotate the image if needed (180 degrees for upside-down images)
        rotated_img = img.rotate(180, expand=True)
        rotated_img.save(image_path)

def extract_images_from_pdf(pdf_path, output_folder):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Iterate through each page
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        images = page.get_images(full=True)
        
        for img_index, img in enumerate(images):
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            image_filename = f"page_{page_num + 1}_img_{img_index + 1}.{image_ext}"
            image_path = os.path.join(output_folder, image_filename)
            
            # Save the image
            with open(image_path, "wb") as image_file:
                image_file.write(image_bytes)
            
            # Correct orientation if needed
            correct_orientation(image_path)
    
    print(f"Images extracted to {output_folder}")

# Example usage
pdf_path = "pdfs"
output_folder = "pdf_imgs"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
# cleaning the output folder
for f in os.listdir(output_folder):
    os.remove(os.path.join(output_folder, f))

pdfs = [f for f in os.listdir(pdf_path) if f.endswith(".pdf") or f.endswith(".PDF")]
for i in pdfs:
    location = os.path.join(pdf_path, i)
    extract_images_from_pdf(location, output_folder)

print("Resizing images...")
subprocess.run(["python", "resizePdfImg.py"])
