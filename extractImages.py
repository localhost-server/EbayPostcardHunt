import os
import subprocess
import shutil

def extract_images_using_pdftohtml(pdf_path, output_folder):
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Extract images using pdftohtml
    for pdf_file in os.listdir(pdf_path):
        if pdf_file.endswith(".pdf") or pdf_file.endswith(".PDF"):
            full_pdf_path = os.path.join(pdf_path, pdf_file)
            # Run the pdftohtml command to extract images
            subprocess.run(["pdftohtml", "-c", "-hidden", "-nodrm", full_pdf_path, output_folder])
    
    print(f"Images extracted to {output_folder}")

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
