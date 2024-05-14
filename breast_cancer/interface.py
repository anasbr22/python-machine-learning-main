import tkinter as tk
from tkinter import filedialog
import pandas as pd
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import matplotlib.colors as mcolors
import sys
import joblib





scaler = joblib.load('model/scaler.pkl')
svm_model = joblib.load('model/svm_model.pkl')




win = tk.Tk()
win.geometry("1100x600+100+10")
background_image = Image.open("img/background.jpg")
background_photo = ImageTk.PhotoImage(background_image)
background_label = tk.Label(win, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)


row_entries = []
inputs = [[17.99, 10.38, 122.8, 1001, 0.1184, 0.2776, 0.3001, 0.1471, 0.2419, 0.07871, 1.095, 0.9053, 8.589, 153.4, 0.006399, 0.04904, 0.05373, 0.01587, 0.03003, 0.006193, 25.38, 17.33, 184.6, 2019, 0.1622, 0.6656, 0.7119, 0.2654, 0.4601, 0.1189]]
features = [
    "radius_mean", "texture_mean", "perimeter_mean", "area_mean", "smoothness_mean",
    "compactness_mean", "concavity_mean", "concave points_mean", "symmetry_mean", "fractal_dimension_mean",
    "radius_se", "texture_se", "perimeter_se", "area_se", "smoothness_se",
    "compactness_se", "concavity_se", "concave points_se", "symmetry_se", "fractal_dimension_se",
    "radius_worst", "texture_worst", "perimeter_worst", "area_worst", "smoothness_worst",
    "compactness_worst", "concavity_worst", "concave points_worst", "symmetry_worst", "fractal_dimension_worst"
]



def on_mousewheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

def on_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))




label_tit = tk.Label(win, text="Classification de tumeur du Sein", font=("Helvetica", 33))
label_tit.place(relx=0.5, y=30, anchor="center")
label_tit.config(bg=background_label.cget('bg'))  

main_frame = ttk.Frame(win)
main_frame.place(x=70, y=80)

scrollbar = ttk.Scrollbar(main_frame, orient="vertical")
scrollbar.pack(side=tk.RIGHT, fill=tk.Y, expand=False)

canvas = tk.Canvas(main_frame, yscrollcommand=scrollbar.set, width=940)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar.config(command=canvas.yview)

input_frame = ttk.Frame(canvas)
canvas.create_window((0,0), window=input_frame, anchor="nw")

background_image2 = Image.open("img/background2.jpg")
background_photo2 = ImageTk.PhotoImage(background_image2)
background_label2 = tk.Label(input_frame, image=background_photo2)
background_label2.place(x=0, y=0, relwidth=1, relheight=1)




entries = None
def create_input_fields():
    global row_entries
    global entries
    num_rows = len(features) // 3  
    extra_row = len(features) % 3  

    entries = []
    for i in range(num_rows):
        row_entries = []
        for j in range(3):
            index = i * 3 + j
            label = ttk.Label(input_frame, text=f"{features[index]}:", font=("Helvetica", 9, "bold"))
            label.grid(row=i, column=j * 2, padx=5, pady=5, sticky="w")
            entry = ttk.Entry(input_frame)
            entry.grid(row=i, column=j * 2 + 1, padx=5, pady=5, sticky="ew")
            row_entries.append(entry)
        entries.append(row_entries)
    
    if extra_row > 0:
        row_entries = []
        start_index = num_rows * 3
        for j in range(extra_row):
            index = start_index + j
            label = ttk.Label(input_frame, text=f"{features[index]}:", font=("Helvetica", 9, "bold"))
            label.grid(row=num_rows, column=j * 2, padx=5, pady=5, sticky="w")
            entry = ttk.Entry(input_frame)
            entry.grid(row=num_rows, column=j * 2 + 1, padx=5, pady=5, sticky="ew")
            row_entries.append(entry)
        entries.append(row_entries)

    return entries

entries = create_input_fields()





canvas.bind("<Configure>", on_configure)
canvas.bind_all("<MouseWheel>", on_mousewheel)

def charger_exemple():
    i = 0
    for entry_row in entries:
        for entry in entry_row:
            entry.delete(0, "end")  
            entry.insert(0, inputs[0][i]) 
            i += 1

def reset():
    global text_affichage
    i = 0
    for entry_row in entries:
        for entry in entry_row:
            entry.delete(0, "end")  
            entry.insert(0, "") 
            i += 1
    
    text_affichage.config(state=tk.NORMAL)
    text_affichage.delete("1.0", tk.END)
    text_affichage.config(state=tk.DISABLED)

button_exemple = tk.Button(win, text="Exemple", width=12, font=('Arial', 14), bg="#F1F1F1", command=charger_exemple)
button_reset = tk.Button(win, text="Reset", width=12, font=('Arial', 14), fg="red", bg="#F1F1F1", command=reset)

button_exemple.place(x=70, y=370)
button_reset.place(x=470, y=370)

affichage_frame = tk.Frame(win)
affichage_frame.place(relx=0.5, y=500, anchor="center")

scrollbar_affichage = ttk.Scrollbar(affichage_frame, orient="vertical")
scrollbar_affichage.pack(side=tk.RIGHT, fill=tk.Y)

text_affichage = tk.Text(affichage_frame, font=('Arial', 11), bg="#F1F1F1", width=70, height=5, yscrollcommand=scrollbar_affichage.set, wrap="word", state=tk.DISABLED, borderwidth=0, highlightthickness=0)
text_affichage.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar_affichage.config(command=text_affichage.yview)




def valide_pr(tab):
    for i, val in enumerate(tab):
        if val and not val.isdigit():
            try:
                float(val)  
            except ValueError:
                return [False, i]
    return [True, None]



def valider():
    global entries
    global text_affichage

    input_val = []
    
    for entry_row in entries:
        for entry in entry_row:

            input_val.append(entry.get())
    
    tab_verif=valide_pr(input_val)
    if(tab_verif[0]):
        inputs_scaled = scaler.transform([input_val])

        prediction = svm_model.predict(inputs_scaled)

        result = 'Malignant' if prediction[0] == 1 else 'Benign'
        text = "Resultat de Prediction :  " + result
        text_affichage.config(state=tk.NORMAL)
        text_affichage.delete("1.0", tk.END)
        text_affichage.insert(tk.END, text)
        text_affichage.config(state=tk.DISABLED)

    else:
        txt2=f"Entrer invalide : {tab_verif[1]} "
        text_affichage.config(state=tk.NORMAL)
        text_affichage.delete("1.0", tk.END)
        text_affichage.insert(tk.END, txt2)
        text_affichage.config(state=tk.DISABLED)








  



button_validate = tk.Button(win, text="Validate", width=12, font=('Arial', 14,'bold'), fg="green", bg="#F1F1F1", command=valider)
button_validate.place(x=270, y=370)

def load_and_display_model_info():
    global scaler 
    global svm_model 

    svm_info = (
        f"SVM Classes: {svm_model.classes_}\n"
        f"SVM Support Vectors: {svm_model.support_}\n"
        f"SVM Number of Support Vectors: {svm_model.n_support_}\n"
        f"SVM Intercept: {svm_model.intercept_}\n"
        f"SVM Parameters: {svm_model.get_params()}\n"
    )

    text_affichage.config(state=tk.NORMAL)
    text_affichage.delete("1.0", tk.END)
    text_affichage.insert(tk.END, svm_info)
    text_affichage.config(state=tk.DISABLED)

button_info = tk.Button(win, text="Info Model", width=12, font=('Arial', 14), fg="#607274", bg="#F1F1F1", command=load_and_display_model_info)
button_info.place(x=670, y=370)

win.mainloop()
