import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from pdf2image import convert_from_path
import easyocr
import numpy as np
import os
import sys

# 🗂 Resolve base directory (for EXE or normal .py run)
BASE_DIR = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

# 🔧 Set paths to resources inside the app folder
POPPLER_PATH = os.path.join(BASE_DIR, 'poppler', 'Library', 'bin')
os.environ['EASYOCR_MODULE_PATH'] = os.path.join(BASE_DIR, '.EasyOCR')

# 🔍 Initialize EasyOCR reader
reader = easyocr.Reader(['en'], gpu=False)

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("Image/PDF files", "*.png *.jpg *.jpeg *.bmp *.tiff *.pdf")])
    if not file_path:
        return

    if file_path.lower().endswith(".pdf"):
        images = convert_from_path(file_path, poppler_path=POPPLER_PATH)
        image = images[0]  # First page only
    else:
        image = Image.open(file_path)

    # Display image
    display_image = image.copy()
    display_image.thumbnail((400, 400))
    img_tk = ImageTk.PhotoImage(display_image)
    image_label.config(image=img_tk)
    image_label.image = img_tk

    # OCR
    image_np = np.array(image.convert("RGB"))
    results = reader.readtext(image_np)
    extracted_text = "\n".join([res[1] for res in results])

    # Show text
    text_box.delete("1.0", tk.END)
    text_box.insert(tk.END, extracted_text)

# GUI setup
root = tk.Tk()
root.title("OCR - Offline")
root.geometry("600x600")

tk.Button(root, text="Select Passport/ID Image or PDF", command=select_file).pack(pady=10)
image_label = tk.Label(root)
image_label.pack()
text_box = tk.Text(root, wrap='word', height=15)
text_box.pack(expand=True, fill='both', padx=10, pady=10)

root.mainloop()
