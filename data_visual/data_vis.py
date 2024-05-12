import tkinter as tk
from tkinter import filedialog
import pandas as pd
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import matplotlib.colors as mcolors



win = tk.Tk()
win.geometry("1100x600+100+10")

background_image = Image.open("img/background.jpg")
background_photo = ImageTk.PhotoImage(background_image)

background_label = tk.Label(win, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1) 



df = None
canvas1,canvas2,canvas3=None,None,None
axe1,axe2,axe3,fig1,fig2,fig3=None,None,None,None,None,None

def read_csv():
    global button_txt, label_alert, label_selected_file, df,button_validate,select_param,select_attr
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        reset()
        df = pd.read_csv(file_path)
        df_numerical = df.select_dtypes(include='number') 
        update_combobox_values(df_numerical)
        button_txt.config(state="disabled")
        label_alert.config(text="File downloaded \n successfully")
        label_selected_file.config(text=f"File :  {file_path}")
        button_validate.config(state="active")
        select_param.config(state="active")
        select_attr.config(state="active")
        select_color.config(state="active")
        select_edgcol.config(state="active")
        select_alpha.config(state="active")
        text_label.delete(0, tk.END)
        text_label.configure(state="normal")
        select_color.set("blue")
        select_edgcol.set("black")
        select_alpha.set(1)


    else:
        label_alert.config(text="download failure")
        label_selected_file.config(text="File : ")

def read_txt():
    global button_csv, label_alert, label_selected_file, df,button_validate
    file_path = filedialog.askopenfilename(filetypes=[("TXT files", "*.txt")])
    if file_path:
        reset()
        df = pd.read_csv(file_path, delimiter='\t')
        df_numerical = df.select_dtypes(include='number')  
        update_combobox_values(df_numerical)
        button_csv.config(state="disabled")
        label_alert.config(text="File downloaded \n successfully")
        label_selected_file.config(text=f"File :  {file_path}")
        button_validate.config(state="active")
        select_param.config(state="active")
        select_attr.config(state="active")
        select_color.config(state="active")
        select_edgcol.config(state="active")
        select_alpha.config(state="active")
        text_label.delete(0, tk.END)
        text_label.configure(state="normal")
        select_color.set("blue")
        select_edgcol.set("black")
        select_alpha.set(1)

        
    else:
        label_alert.config(text="download failure")
        label_selected_file.config(text="File : ")

def update_combobox_values(df):
    global available_columns
    available_columns = list(df.columns)
    selet_x['values'] = available_columns
    selet_y['values'] = available_columns
    select_attr['values'] = available_columns

def on_combobox_change(event):
    global available_columns
    selected_value = event.widget.get()
    if selected_value:
        available_columns_copy = available_columns.copy()
        available_columns_copy.remove(selected_value)

        if selet_x.get() != selected_value:
            selet_x['values'] = available_columns_copy
        if selet_y.get() != selected_value:
            selet_y['values'] = available_columns_copy
    else:
        selet_x['values'] = available_columns
        selet_y['values'] = available_columns

def destroy():
    global canvas3,canvas2,canvas1
    canvases = [canvas1, canvas2, canvas3]  
    for canvas in canvases:
        if canvas:
            canvas.get_tk_widget().destroy()


def reset():
    global label_alert, label_selected_file, button_csv, button_txt, selet_x, selet_y,button_validate,label_disp_par,tcolor,tedgcolor,talpha,tlabel
    label_alert.config(text="")
    label_selected_file.config(text="")
    selet_x.config(values=[])
    selet_x.set("") 
    selet_y.config(values=[])
    selet_y.set("")
    button_csv.config(state="active")
    button_txt.config(state="active")
    plot_empty()
    destroy()
    button_validate.config(state="disabled")
    select_param.config(state="disabled")
    select_attr.config(state="disabled")
    label_disp_par.config(text="")
    select_color.config(state="disabled")
    select_edgcol.config(state="disabled")
    select_alpha.config(state="disabled")
    text_label.delete(0, tk.END)
    text_label.configure(state="disabled")
    tcolor,tedgcolor,talpha,tlabel=None,None,None,None
    

   


def validate():
    global label_type_graph, df,label_alert
    graph_type = select_graph.get()
    if graph_type == "Histogramme":
        plot_histogram(df)
    elif graph_type == "Nuage des points":
        plot_scatter(df)
    elif graph_type == "Diagramme en boîte":
        plot_box(df)
    else:
        label_alert.config(text="Diagramme not \n found")



def plot_empty():
    image_path = "img/empty.png"
    img = Image.open(image_path)
    
    width, height = img.size
    new_width = 300
    new_height = int(height * (new_width / width))
    img = img.resize((new_width, new_height))
    
    img_tk = ImageTk.PhotoImage(img)
    
    canvas = tk.Canvas(win, width=633, height=473, borderwidth=2, relief="solid")
    
    x = (633 - new_width) // 2
    y = (473 - new_height) // 2
    
    canvas.create_image(x, y, anchor="nw", image=img_tk)
    canvas.place(x=200, y=10)
    
    canvas.img_tk = img_tk


tcolor,tedgcolor,talpha,tlabel="blue","black",1.0,""

def plot_histogram(df, color='blue', edgecolor='black', alpha=1.0, label=None):
    global canvas1,label_alert

    destroy()

    x = selet_x.get()
    if x:
        fig1, axe1 = plt.subplots()
        axe1.hist(df[x], color=color, edgecolor=edgecolor, alpha=alpha, label=label)
        plt.xlabel('X-value')
        plt.legend()
        canvas1 = FigureCanvasTkAgg(fig1, master=win)
        canvas1.draw()
        canvas1.get_tk_widget().place(x=200, y=10)
        canvas1.get_tk_widget().config(borderwidth=2, relief="solid")
        label_alert.config(text="Histogram Plot")
        
    else:
        label_alert.config(text="x-value missing")


def plot_scatter(df,color='blue', edgecolor='black', alpha=1.0, label=None):
    global canvas2,label_alert

    destroy()

    x = selet_x.get()
    y = selet_y.get()
    if x and y:
        fig2, axe2 = plt.subplots()
        axe2.scatter(df[x], df[y],color=color, edgecolor=edgecolor, alpha=alpha, label=label)
        plt.xlabel('X-value')
        plt.ylabel('Y-value')
        plt.legend()
        canvas2 = FigureCanvasTkAgg(fig2, master=win)
        canvas2.draw()
        canvas2.get_tk_widget().place(x=200, y=10)
        canvas2.get_tk_widget().config(borderwidth=2, relief="solid")
        label_alert.config(text="Scatter plot")
    else:
        label_alert.config(text="(x-value or y-value) \n missing")

def plot_box(df,color='blue', edgecolor='black', alpha=1.0, label=None):
    global canvas3,label_alert

    destroy()

    x = selet_x.get()
    if x:
        fig3, axe3 = plt.subplots()
        axe3.boxplot(df[x],patch_artist=True)
        axe3.set_facecolor(color)
        plt.xlabel('X-value')
        plt.legend()
        canvas3 = FigureCanvasTkAgg(fig3, master=win)
        canvas3.draw()
        canvas3.get_tk_widget().place(x=200, y=10)
        canvas3.get_tk_widget().config(borderwidth=2, relief="solid")
        label_alert.config(text="Box plot")
    else:
        label_alert.config(text="x-value missing")






def update_plot(event):
    """Fonction pour mettre à jour le graphique en fonction des nouvelles valeurs."""
    global select_graph, select_color, select_edgcol, select_alpha, text_label
    tcolor = select_color.get()
    tedgcolor = select_edgcol.get()
    talpha = float(select_alpha.get())
    tlabel = text_label.get()
    type_gr = select_graph.get()
    
    if type_gr == "Histogramme":
        plot_histogram(df, color=tcolor, edgecolor=tedgcolor, alpha=talpha, label=tlabel)
    elif type_gr == "Nuage des points":
        plot_scatter(df, color=tcolor, edgecolor=tedgcolor, alpha=talpha, label=tlabel)
    elif type_gr == "Diagramme en boîte":
        plot_box(df, color=tcolor, edgecolor=tedgcolor, alpha=talpha, label=tlabel)

def set_color(event):
    update_plot(event)

def set_edgcol(event):
    update_plot(event)

def set_alpha(event):
    update_plot(event)

def set_label(event):
    update_plot(event)
    text_label.focus()
    text_label.focus_force()



   

#  moyenne
def calculer_moyenne(donnees):
    return pd.Series(donnees).mean()

#  la médiane
def calculer_mediane(donnees):
    return pd.Series(donnees).median()

#  le mode
def calculer_mode(donnees):
    return pd.Series(donnees).mode()

#  l'écart-type
def calculer_ecart_type(donnees):
    return pd.Series(donnees).std()

#  la variance
def calculer_variance(donnees):
    return pd.Series(donnees).var()

#  les quartiles
def calculer_quartiles(donnees):
    return pd.Series(donnees).quantile([0.25, 0.5, 0.75])




def display_parameter_value():
    selected_param = select_param.get()
    selected_attr = select_attr.get()
    if selected_param and selected_attr:
        if selected_param == "median":
            value = calculer_mediane(df[selected_attr])
        elif selected_param == "mode":
            value = calculer_mode(df[selected_attr])
        elif selected_param == "ecart-type":
            value = calculer_ecart_type(df[selected_attr])
        elif selected_param == "variance":
            value = calculer_variance(df[selected_attr])
        elif selected_param == "Quartiles":
            value = calculer_quartiles(df[selected_attr])
        elif selected_param == "mean":
            value = calculer_moyenne(df[selected_attr])
        else:
            value = ""
        label_disp_par.config(text=str(value))
    else:
        label_disp_par.config(text="")

def on_select_param(event):
    display_parameter_value()


import tkinter as tk
from tkinter import ttk

def display_table():
    global df

    if df is not None:
        top = tk.Toplevel()
        top.title("Imported Table")
        
        frame = ttk.Frame(top)
        frame.pack(fill=tk.BOTH, expand=True)
        
        
        table = ttk.Treeview(frame)
        table['columns'] = tuple(df.columns)
        table['show'] = 'headings'
        for column in df.columns:
            table.heading(column, text=column)
        for index, row in df.iterrows():
            table.insert('', 'end', values=tuple(row))
        
       
        yscroll = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=table.yview)
        yscroll.pack(side=tk.RIGHT, fill=tk.Y)
        table.configure(yscrollcommand=yscroll.set)
        
        xscroll = ttk.Scrollbar(frame, orient=tk.HORIZONTAL, command=table.xview)
        xscroll.pack(side=tk.BOTTOM, fill=tk.X)
        table.configure(xscrollcommand=xscroll.set)
        
        table.pack(expand=tk.YES, fill=tk.BOTH)
    else:
        label_alert.config(text="No data imported yet!")







button_csv = tk.Button(win, text="Read .csv", height=2, bg="#B5C0D0", command=read_csv)
button_csv.place(x=10, y=10)

button_txt = tk.Button(win, text="Read .txt", height=2, bg="#B5C0D0", command=read_txt)
button_txt.place(x=100, y=10)

button_validate = tk.Button(win, text="Validate", width=12,state="disabled", font=('Arial', 14), fg="green",bg="#B5C0D0", command=validate)
button_reset = tk.Button(win, text="Reset", width=12, font=('Arial', 14), fg="red",bg="#B5C0D0", command=reset)

button_display_table = tk.Button(win, text="Display Table" ,width=12,font=('Arial', 14),bg="#B5C0D0", command=display_table)


label_alert = tk.Label(win, font=("Arial", 10), width=18, padx=1, pady=5, bg="#B5C0D0",borderwidth=1, relief="solid")
label_x = tk.Label(win, text="X-value", font=("Arial", 12))
label_y = tk.Label(win, text="Y-value", font=("Arial", 12))
label_type_graph = tk.Label(win, text="Graph Type", font=("Arial", 12))
label_selected_file = tk.Label(win, font=("Arial", 8, "bold"), bg="#B5C0D0")
label_attr=tk.Label(win, text="Attribut", font=("Arial", 12,"bold"))
label_param=tk.Label(win, text="Statistical parameters", font=("Arial", 12,"bold"))
label_disp_par=tk.Label(win,width=25,height=5, font=("Arial", 10,"bold"),padx=1, pady=5, bg="#B5C0D0",borderwidth=1, relief="solid")


selet_x = ttk.Combobox(win, width=10, font=('Arial', 12),background="#F1F0E8")
selet_y = ttk.Combobox(win, width=10, font=('Arial', 12),background="#F1F0E8")
select_graph = ttk.Combobox(win, width=14, values=["Histogramme", "Nuage des points", "Diagramme en boîte"], font=('Arial', 12),background="#F1F0E8")
select_graph.set("Histogramme")
select_attr= ttk.Combobox(win, width=15, font=('Arial', 14),state="disabled",background="#F1F0E8")
select_param = ttk.Combobox(win, width=15,values=["","mean","median","mode","ecart-type","variance","Quartiles"], font=('Arial', 14),state="disabled",background="#F1F0E8")
select_param.bind("<<ComboboxSelected>>", on_select_param)

label_color=tk.Label(win, text="Color", font=("Arial", 12,"bold"))
label_edgcol=tk.Label(win, text="EdgColor", font=("Arial", 12,"bold"))
label_alpha=tk.Label(win, text="Alpha", font=("Arial", 12,"bold"))
label_label=tk.Label(win, text="Label", font=("Arial", 12,"bold"))

select_color=ttk.Combobox(win, width=14,values= list(mcolors.CSS4_COLORS.keys()), font=('Arial', 13),state="disabled",background="#F1F0E8")
select_edgcol=ttk.Combobox(win, width=14,values= list(mcolors.CSS4_COLORS.keys()), font=('Arial', 13),state="disabled",background="#F1F0E8")
select_alpha=ttk.Combobox(win, width=14,values= [0.1,0.2,0.4,0.5,0.6,0.8,1], font=('Arial', 13),state="disabled",background="#F1F0E8")
text_label=  tk.Entry(win, width=15, font=('Arial', 13), state="disabled", borderwidth=1, relief="solid", background="#F1F0E8")

select_color.set("blue")
select_edgcol.set("black")
select_alpha.set(1)

select_color.bind("<<ComboboxSelected>>", set_color)
select_edgcol.bind("<<ComboboxSelected>>", set_edgcol)
select_alpha.bind("<<ComboboxSelected>>", set_alpha)
text_label.bind("<KeyRelease>", set_label)


label_alert.place(x=10, y=65)
label_x.place(x=10, y=115)
selet_x.place(x=10, y=145)
label_y.place(x=10, y=178)
selet_y.place(x=10, y=205)
label_attr.place(x=870, y=20)
select_attr.place(x=870, y=50)
label_param.place(x=870, y=80)
select_param.place(x=870, y=110)
label_disp_par.place(x=870, y=155)

label_color.place(x=870, y=260)
select_color.place(x=870, y=285)
label_edgcol.place(x=870, y=315)
select_edgcol.place(x=870, y=340)
label_alpha.place(x=870, y=370)
select_alpha.place(x=870, y=395)
label_label.place(x=870, y=425)
text_label.place(x=870, y=450)


label_type_graph.place(x=10, y=325)
select_graph.place(x=10, y=355)

button_validate.place(x=10, y=385)
button_reset.place(x=10, y=435)
button_display_table.place(x=10, y=480)

label_selected_file.pack(side="bottom", fill="x")

selet_x.bind("<<ComboboxSelected>>", on_combobox_change)
selet_y.bind("<<ComboboxSelected>>", on_combobox_change)

def on_closing():
    win.destroy()
    win.quit()


plot_empty()
win.protocol("WM_DELETE_WINDOW", on_closing)
win.mainloop()
