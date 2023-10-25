import tkinter as tk
from tkinter import filedialog
import json
import requests 


def save_to_json(product_data):
    with open('products.json', 'w') as file:
        json.dump(product_data, file, indent=4)


def load_from_json():
    try:
        with open('products.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def update_product_listbox():
    product_listbox.delete(0, tk.END)
    for product in product_data:
        product_listbox.insert(tk.END, product['name'])

def agregar_producto():
    nombre = nombre_entry.get()
    descripcion = descripcion_entry.get()
    video = video_entry.get()
    if nombre and descripcion and video:
        product = {'name': nombre, 'description': descripcion, 'video': video}
        product_data.append(product)
        save_to_json(product_data)
        update_product_listbox()
        nombre_entry.delete(0, tk.END)
        descripcion_entry.delete(0, tk.END)
        video_entry.delete(0, tk.END)

        response = requests.post(f'{SERVER_URL}/api/products', json=product)
        if response.status_code != 201:
            print('Failed to add the product:', response.status_code)
        else:
            print('Product added successfully')

def editar_producto():
    selected_index = product_listbox.curselection()
    if selected_index:
        index = selected_index[0]
        nombre = nombre_entry.get()
        descripcion = descripcion_entry.get()
        video = video_entry.get()
        if nombre and descripcion and video:
            product = {'name': nombre, 'description': descripcion, 'video': video}
            product_data[index] = product
            save_to_json(product_data)
            update_product_listbox()
            nombre_entry.delete(0, tk.END)
            descripcion_entry.delete(0, tk.END)
            video_entry.delete(0, tk.END)

            try:
                response = requests.put(f'http://localhost:5000/api/products/{index}', json=product)
                response.raise_for_status()  # Raise an exception if status code is not 2xx
                print('Product edited successfully')
            except requests.exceptions.HTTPError as err:
                print(f'Failed to edit the product: {err}')



def eliminar_producto():
    selected_index = product_listbox.curselection()
    if selected_index:
        index = selected_index[0]
        del product_data[index]
        save_to_json(product_data)
        update_product_listbox()
        nombre_entry.delete(0, tk.END)
        descripcion_entry.delete(0, tk.END)
        video_entry.delete(0, tk.END)


        response = requests.delete(f'http://localhost:5000/api/products/{index}')
        if response.status_code != 200:
            print('Failed to delete the product:', response.status_code)
        else:
            print('Product deleted successfully')

def cargar_video():
    file_path = filedialog.askopenfilename(filetypes=[("Archivos de video", "*.mp4 *.avi")])
    video_entry.delete(0, tk.END)
    video_entry.insert(0, file_path)

product_data = load_from_json()

root = tk.Tk()
root.title("Gestión de Productos")

nombre_label = tk.Label(root, text="Nombre del Producto:")
nombre_entry = tk.Entry(root, width=50)

descripcion_label = tk.Label(root, text="Descripción:")
descripcion_entry = tk.Entry(root, width=50)

video_label = tk.Label(root, text="Video:")
video_entry = tk.Entry(root, width=40)
cargar_video_button = tk.Button(root, text="Cargar Video", command=cargar_video)

agregar_button = tk.Button(root, text="Agregar Producto", command=agregar_producto)
editar_button = tk.Button(root, text="Editar Producto", command=editar_producto)
eliminar_button = tk.Button(root, text="Eliminar Producto", command=eliminar_producto)

product_listbox = tk.Listbox(root, width=50)
update_product_listbox()

nombre_label.grid(row=0, column=0, padx=10, pady=10)
nombre_entry.grid(row=0, column=1, padx=10, pady=10)
descripcion_label.grid(row=1, column=0, padx=10, pady=10)
descripcion_entry.grid(row=1, column=1, padx=10, pady=10)
video_label.grid(row=2, column=0, padx=10, pady=10)
video_entry.grid(row=2, column=1, padx=10, pady=10)
cargar_video_button.grid(row=2, column=2, padx=10, pady=10)

product_listbox.grid(row=3, column=0, columnspan=3, padx=10, pady=10)
agregar_button.grid(row=4, column=0, pady=10)
editar_button.grid(row=4, column=1, pady=10)
eliminar_button.grid(row=4, column=2, pady=10)

root.mainloop()
