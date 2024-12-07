import tkinter as tk
from tkinter import filedialog,messagebox
from PIL import ImageFont,ImageDraw,Image,ImageTk

root = tk.Tk()
root.title("watermark application")
root.geometry("800x600")

upload_image = None
def upload():

    global upload_image
    file_path = filedialog.askopenfilename(
        filetypes=[("Image File","*.jpg;*.jpeg;*.png")]
    )
    if file_path:
        upload_image = Image.open(file_path)
        img_tumbnail = upload_image.copy()
        img_tumbnail.thumbnail((700,700))
   

    if file_path:
        upload_image = Image.open(file_path)
        image_thumbnail = upload_image.copy()
        image_thumbnail.thumbnail((700,700))
        image_display = ImageTk.PhotoImage(image_thumbnail)
        image_label.config(image = image_display)
        image_label.image = image_display
        messagebox.showinfo("success","Image successfully uploaded")

def add_logo():
    global upload_image

    logo_path = filedialog.askopenfilename(filetypes=[("Image File","*,jpg;*.jpeg;*png")])
    if logo_path:
        logo = Image.open(logo_path)
        logo.thumbnail((200,200))

    watermark_image = upload_image.copy()

    x = watermark_image.width - logo.width -10
    y = watermark_image.height - logo.height -10

    watermark_image.paste(logo,(x,y),logo if logo.mode == "RGBA"else None) 
    watermark_image.show()
    save_image(watermark_image)
def add_text():
    global upload_image
    if upload_image == None:
        messagebox.showinfo("error","please upload an image first")
        return
    
    watermark_text = text_label.get()
    if not watermark_text:
        messagebox.showinfo("Information","please provide a text first")
        return
    watermark_img = upload_image.copy()
    font = ImageFont.truetype("arial.ttf",36)        
    draw = ImageDraw.Draw(watermark_img)    

     
    text_bbox = draw.textbbox((0,0),watermark_text,font = font) 
    text_height, text_width = text_bbox[3] - text_bbox[1], text_bbox[2] - text_bbox[0]

    x = watermark_img.width - text_width - 10
    y = watermark_img.height - text_height -10
    draw.text((x,y),watermark_text,(255,255,255),font = font)

    watermark_img.show()
    save_image(watermark_img)

def save_image(image):
    save_path = filedialog.asksaveasfilename(filetypes=[("PNG file",".png")])

    if save_path:
        image.save(save_path)
        messagebox.showinfo("Success","file saved succesfully")

upload_btn = tk.Button(root,text = "upload image",command=upload)
upload_btn.pack(pady=10)

logo_btn = tk.Button(root,text = "add logo",command=add_logo)
logo_btn.pack(pady=10)

text_label = tk.Entry(root)
text_label.insert(0,"write here")
text_label.pack(pady=10)

text_button = tk.Button(root,text = "add text",command=add_text)
text_button.pack(pady=10)

image_label = tk.Label(root)
image_label.pack(pady=10)

root.mainloop()
