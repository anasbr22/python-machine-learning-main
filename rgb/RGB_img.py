import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2 as cv
import numpy as np

# Fonction de redimensionnement
def resize(image, new_width):
    width, height = image.size
    new_height = int(height * (new_width / width))
    return image.resize((new_width, new_height))


# Fonction pour charger une image
def load_image():
    global img, mat_img

    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])

    if file_path:
        try:
            image = Image.open(file_path)
            mat_img = cv.imread(file_path)
            print(mat_img.shape)
            
            image = resize(image, 500)
            img = ImageTk.PhotoImage(image)

            label.configure(image=img)
            label.image = img
        except Exception as e:
            print(f"Erreur lors du chargement de l'image : {e}")

# Fonction pour modifier les canaux RGB de l'image
def change(event=None):
    global mat_img
    global scale
    global scale2
    global scale3
    global label

    pr = scale.get()
    pg = scale2.get()
    pb = scale3.get()

    if mat_img is not None:
        m_red = np.array(mat_img[:, :, 0])
        m_green = np.array(mat_img[:, :, 1])
        m_blue = np.array(mat_img[:, :, 2])

    
        m_red_mod = (m_red + ((255-m_red)*(pr/100))).astype(np.uint8) if pr >= 0 else (m_red + ((m_red)*(pr/100))).astype(np.uint8)
            
        m_green_mod = (m_green + ((255-m_green)*(pg/100))).astype(np.uint8) if pg >= 0 else (m_green + ((m_green)*(pg/100))).astype(np.uint8)
            
        m_blue_mod = (m_blue + ((255-m_blue)*(pb/100))).astype(np.uint8) if pb >= 0 else (m_blue + ((m_blue)*(pb/100))).astype(np.uint8)


        mat_modifier = np.stack((m_red_mod, m_green_mod, m_blue_mod), axis=-1)

        img_modified = Image.fromarray(mat_modifier)
        img_modified_resized = resize(img_modified, 500)

        img_mod = ImageTk.PhotoImage(img_modified_resized)
        label.configure(image=img_mod)
        label.image = img_mod


# Fonction pour réinitialiser les modifications
def reset():
    global img

    scale.set(0)
    scale2.set(0)
    scale3.set(0)

    if img:
        label.config(image=img)
        label.image=img
    

# Fonction pour sauvegarder l'image modifiée
def save_image():
    global mat_img

    if mat_img is not None:
        file_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png")])
        if file_path:
            cv.imwrite(file_path, cv.cvtColor(mat_img, cv.COLOR_RGB2BGR))

# Interface graphique
win = tk.Tk()
win.title("Importateur d'images")
win.geometry("800x500")

bk_path = "img/bk.jpg"

bk_img = Image.open(bk_path)
bk_image = ImageTk.PhotoImage(resize(bk_img, 250))

label = tk.Label(win, width=500, image=bk_image)
label.grid(row=1, column=2)

load_button = tk.Button(win, text="Charger une image", command=load_image)
load_button.grid(row=1, column=1)

lr = tk.Label(text="Red (%)", fg="red")
lg = tk.Label(text="Green (%)", fg="green")
lb = tk.Label(text="Blue (%)", fg="blue")

lr.grid(row=3, column=1)
lg.grid(row=4, column=1)
lb.grid(row=5, column=1)

scale = tk.Scale(win, from_=-100, to=100, orient=tk.HORIZONTAL, length=230, fg="red", command=change)
scale.grid(row=3, column=2)
scale2 = tk.Scale(win, from_=-100, to=100, orient=tk.HORIZONTAL, length=230, fg="green", command=change)
scale2.grid(row=4, column=2)
scale3 = tk.Scale(win, from_=-100, to=100, orient=tk.HORIZONTAL, length=230, fg="blue", command=change)
scale3.grid(row=5, column=2)

save_button = tk.Button(win, text="Sauvegarder", command=save_image)
save_button.grid(row=2, column=1)
reset_button = tk.Button(win, text="Réinitialiser", command=reset)
reset_button.grid(row=2, column=2)

win.mainloop()


