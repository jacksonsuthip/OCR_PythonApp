import tkinter as tk
from tkinter import filedialog, Toplevel
from PIL import Image, ImageTk
from pdf2image import convert_from_path
import easyocr
import numpy as np
import os

BASE_DIR = os.path.dirname(__file__)
POPPLER_PATH = os.path.join(BASE_DIR, "poppler", "Library", "bin")
ICON_PATH = os.path.join(BASE_DIR, "ocr_icon.ico")  # Your .ico icon path

reader = easyocr.Reader(['en'], gpu=False)

def show_full_image(img):
    top = Toplevel(root)
    top.title("Full Image Preview")

    # Maximize window (works on Windows and Linux)
    top.state('zoomed')  # Use 'zoomed' to maximize window

    # Get screen size
    screen_width = top.winfo_screenwidth()
    screen_height = top.winfo_screenheight()

    # Resize image to fit screen while maintaining aspect ratio
    img_copy = img.copy()
    img_copy.thumbnail((screen_width - 100, screen_height - 100))  # Padding of 100px
    full_img = ImageTk.PhotoImage(img_copy)

    lbl = tk.Label(top, image=full_img)
    lbl.image = full_img  # Keep a reference
    lbl.pack(expand=True)

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[
        ("Image/PDF files", "*.png *.jpg *.jpeg *.bmp *.tiff *.pdf")
    ])
    if not file_path:
        return

    file_path_var.set(file_path)
    loading_label.config(text="🔍 Loading...", fg="red")
    root.update_idletasks()

    if file_path.lower().endswith(".pdf"):
        images = convert_from_path(file_path, poppler_path=POPPLER_PATH)
        image = images[0]
    else:
        image = Image.open(file_path)

    display_image = image.copy()
    display_image.thumbnail((200, 200))
    img_tk = ImageTk.PhotoImage(display_image)
    image_label.config(image=img_tk)
    image_label.image = img_tk

    # Bind click to open full image
    image_label.bind("<Button-1>", lambda e: show_full_image(image))

    image_np = np.array(image.convert("RGB"))
    results = reader.readtext(image_np)
    extracted_text = "\n".join([res[1] for res in results])

    text_box.delete("1.0", tk.END)
    text_box.insert(tk.END, extracted_text)

    loading_label.config(text="✅ Done", fg="green")

# --- UI Setup ---
root = tk.Tk()
root.title("OCR App")
root.geometry("700x500")

if os.path.exists(ICON_PATH):
    root.iconbitmap(ICON_PATH)

# App title label
# tk.Label(root, text="🧾 OCR App", font=("Helvetica", 18, "bold")).pack(pady=(10, 0))

top_bar = tk.Frame(root)
top_bar.pack(pady=10)

tk.Button(top_bar, text="📁 Select File", command=select_file).pack(side="left", padx=5)

file_path_var = tk.StringVar()
tk.Entry(top_bar, textvariable=file_path_var, state="readonly", width=60).pack(side="left", padx=5)

loading_label = tk.Label(top_bar, text="", font=("Helvetica", 12))
loading_label.pack(side="left", padx=5)

# Image + Text layout vertically
image_label = tk.Label(root)
image_label.pack(pady=5)

text_box = tk.Text(root, wrap='word', height=15)
text_box.pack(fill="both", expand=True, padx=10, pady=10)

root.mainloop()
