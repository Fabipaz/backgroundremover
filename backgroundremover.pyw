import os
from datetime import datetime
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from rembg import remove

class BackgroundRemover:
    def __init__(self, input_folder, output_folder):
        self.input_folder = input_folder
        self.output_folder = output_folder

    def process_images(self):
        today = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
        processed_folder = os.path.join(self.output_folder, today)
        os.makedirs(processed_folder, exist_ok=True)

        for filename in os.listdir(self.input_folder):
            if filename.endswith(('.png', '.jpg', '.jpeg')):
                input_path = os.path.join(self.input_folder, filename)
                output_path = os.path.join(processed_folder, filename)
                self._remove_background(input_path, output_path)
                self._move_originals(input_path, processed_folder)

    def _remove_background(self, input_p, output_p):
        with open(input_p, 'rb') as inp, open(output_p, 'wb') as outp:
            background_output = remove(inp.read())
            outp.write(background_output)

    def _move_originals(self, input_p, dest_p):
        originals_folder = os.path.join(dest_p, 'originals')
        os.makedirs(originals_folder, exist_ok=True)

        filename = os.path.basename(input_p)
        new_path = os.path.join(originals_folder, filename)
        os.rename(input_p, new_path)

def select_input_folder():
    folder = filedialog.askdirectory()
    input_folder_entry.delete(0, tk.END)
    input_folder_entry.insert(0, folder)

def select_output_folder():
    folder = filedialog.askdirectory()
    output_folder_entry.delete(0, tk.END)
    output_folder_entry.insert(0, folder)

def start_processing():
    input_folder = input_folder_entry.get()
    output_folder = output_folder_entry.get()
    remover = BackgroundRemover(input_folder, output_folder)
    remover.process_images()
    result_label.config(text="Proceso completado", font=("Comic Sans MS", 12))

def open_input_folder():
    input_folder = input_folder_entry.get()
    if os.path.exists(input_folder):
        os.startfile(input_folder)    

def open_output_folder():
    output_folder = output_folder_entry.get()
    if os.path.exists(output_folder):
        os.startfile(output_folder)


# Crear la ventana principal de la aplicación
root = tk.Tk()
root.title("Background Remover by Fabipaz")
root.configure(bg="#F0F0F0")

# Crear y configurar widgets
logo_label = tk.Label(root, text="Background Remover", font=("Comic Sans MS", 50), bg="#F0F0F0")
logo_label.pack(pady=20)
progress_bar = ttk.Progressbar(root, orient="horizontal", mode="determinate",)
progress_bar.pack(pady=10, fill="x")

input_folder_label = tk.Label(root, text="Carpeta de entrada:",font=("Comic Sans MS", 24))
input_folder_label.pack()

input_folder_entry = tk.Entry(root, width=50)
input_folder_entry.pack()

input_folder_button = tk.Button(root, text="Seleccionar carpeta de entrada", command=select_input_folder, bg="#007ACC", fg="white")
input_folder_button.pack(pady=5)

output_folder_label = tk.Label(root, text="Carpeta de salida:", font=("Comic Sans MS", 24))
output_folder_label.pack()

output_folder_entry = tk.Entry(root, width=50)
output_folder_entry.pack()

output_folder_button = tk.Button(root, text="Seleccionar carpeta de salida", command=select_output_folder, bg="#007ACC", fg="white")
output_folder_button.pack(pady=50)

process_button = tk.Button(root, text="Iniciar Proceso", command=start_processing, bg="#4CAF50", fg="white")
process_button.pack(pady=10)

open_folder_button = tk.Button(root, text="Validar Carpeta de Salida", command=open_output_folder, bg="#007ACC", fg="white")
open_folder_button.pack(pady=10)

open_folder_button = tk.Button(root, text="Validar Carpeta de entrada", command=open_input_folder, bg="#007ACC", fg="white")
open_folder_button.pack(pady=10)

result_label = tk.Label(root, text="")
result_label.pack()

# Ejecutar la aplicación
root.mainloop()
