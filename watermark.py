import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont

# Initialize the main application window
root = tk.Tk()
root.title("Watermark Application")
root.geometry("800x600")

# Global variable for the uploaded image
uploaded_image = None

# Function to upload an image
def upload_image():
    global uploaded_image
    file_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")]
    )
    if file_path:
        uploaded_image = Image.open(file_path)
        img_thumbnail = uploaded_image.copy()
        img_thumbnail.thumbnail((700, 700))  # Resize for display in GUI
        img_display = ImageTk.PhotoImage(img_thumbnail)
        img_label.config(image=img_display)
        img_label.image = img_display
        messagebox.showinfo("Image Uploaded", "Image successfully uploaded!")

# Function to add watermark text
def add_watermark_text():
    global uploaded_image
    if uploaded_image is None:
        messagebox.showwarning("Warning", "Please upload an image first.")
        return

    watermark_text = watermark_text_entry.get()
    if not watermark_text:
        messagebox.showwarning("Warning", "Please enter watermark text.")
        return

    # Copy the uploaded image to avoid modifying the original
    watermarked_image = uploaded_image.copy()
    draw = ImageDraw.Draw(watermarked_image)
    font = ImageFont.truetype("arial.ttf", 36)
    
    # Calculate the bounding box of the text
    text_bbox = draw.textbbox((0, 0), watermark_text, font=font)
    text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]

    # Position watermark at the bottom right
    x = watermarked_image.width - text_width - 10
    y = watermarked_image.height - text_height - 10
    draw.text((x, y), watermark_text, (255, 255, 255), font=font)

    # Save and display the watermarked image
    watermarked_image.show()
    save_image(watermarked_image)


# Function to add watermark logo
def add_watermark_logo():
    global uploaded_image
    if uploaded_image is None:
        messagebox.showwarning("Warning", "Please upload an image first.")
        return

    logo_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")]
    )
    if logo_path:
        logo = Image.open(logo_path)
        logo.thumbnail((200, 200))  # Resize logo

        # Copy the uploaded image to avoid modifying the original
        watermarked_image = uploaded_image.copy()

        # Position logo at the bottom right
        x = watermarked_image.width - logo.width - 10
        y = watermarked_image.height - logo.height - 10
        watermarked_image.paste(logo, (x, y), logo if logo.mode == 'RGBA' else None)

        # Save and display the watermarked image
        watermarked_image.show()
        save_image(watermarked_image)

# Function to save the watermarked image
def save_image(image):
    save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                             filetypes=[("PNG files", "*.png")])
    if save_path:
        image.save(save_path)
        messagebox.showinfo("Image Saved", f"Image saved to {save_path}")

# Widgets
upload_btn = tk.Button(root, text="Upload Image", command=upload_image)
upload_btn.pack(pady=10)

watermark_text_entry = tk.Entry(root, width=30)
watermark_text_entry.insert(0, "Enter watermark text")
watermark_text_entry.pack(pady=10)

text_watermark_btn = tk.Button(root, text="Add Text Watermark", command=add_watermark_text)
text_watermark_btn.pack(pady=5)

logo_watermark_btn = tk.Button(root, text="Add Logo Watermark", command=add_watermark_logo)
logo_watermark_btn.pack(pady=5)

img_label = tk.Label(root)
img_label.pack(pady=10)

# Start the application
root.mainloop()
