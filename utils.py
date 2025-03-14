# ocr_app/utils.py

import os
import tempfile
import easyocr
import pypdfium2 as pdfium
from PIL import Image
import numpy as np

def handle_uploaded_file(pdf_file):
    
    """Save uploaded PDF file to a temporary directory and return its path."""
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, pdf_file.name)
    with open(file_path, "wb") as f:
        for chunk in pdf_file.chunks():
            f.write(chunk)
    return file_path


def clean_up_file(file_path):
    """Remove the file from the filesystem."""
    if os.path.exists(file_path):
        os.remove(file_path)


def extract_text_with_easyocr(pdf_path):
    extracted_text = ""
    reader = easyocr.Reader(["en"], gpu=False)  # Set languages as needed

    # Open the PDF document
    pdf_document = pdfium.PdfDocument(pdf_path)

    for page_num in range(len(pdf_document)):
        page = pdf_document.get_page(page_num)

        # Render the page as an image and convert to PIL format
        pil_image = page.render(scale=2).to_pil()

        # Convert the PIL image to a NumPy array for EasyOCR
        np_image = np.array(pil_image)

        # Use EasyOCR to extract text from the image
        text = reader.readtext(np_image, detail=0)
        extracted_text += " ".join(text) + "\n"

        # Close the page after processing
        page.close()

    # Manually close the PDF document after finishing all pages
    pdf_document.close()

    return extracted_text
