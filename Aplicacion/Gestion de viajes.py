import tkinter as tk #Le agrego el alias tk a las funciones importadas de la biblioteca tkinter
from tkinter import ttk, messagebox
from PIL import Image, ImageTk  # Viene de la librería Pillow, la cual estaré utilizando para añadir el logo de la empresa a la aplicación
import mysql.connector


# Me conecto a la base de datos
db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    passwd="josegras"
)

# Creo un cursor para la base de datos
c = db.cursor()


# ################################
# FUNCIONES
# ################################




# ################################
# INTERFAZ GRAFICA
# ################################

# Aqui creo la ventana principal
root = tk.Tk() 
root.title("Gestión de Grupos de Viaje - Prácticas Laborales Dencanto Community")
root.geometry("1480x700")


# Aqui cargo la imagen de la logo de ma empresa
imagen_original = Image.open("C:/Users/juanc/Desktop/PRACTICAS/Gestión de viajes/Aplicacion/dencanto-logo.png") 
imagen_redimensionada = imagen_original.resize((150, 102))  # Redimensiono la imagen
logo = ImageTk.PhotoImage(imagen_redimensionada)

# Utilizo esta secuencia para mostrar la imagen en la aplicación
logo_label = ttk.Label(root, image=logo)
logo_label.image = logo 
logo_label.pack(pady=10) # Esto equivale al padding


# Aqui creo las pestañas
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

# ################################
# Creando los marcos de cada pestaña
# ################################

# ------------------------------------------------------------------------------------------
#  Gestión de personas
# ------------------------------------------------------------------------------------------

tab_personas = ttk.Frame(notebook)
notebook.add(tab_personas, text="Personas")

ttk.Label(tab_personas, text="DNI:", font=("verdana", 11)).place(x=50, y=20)
entry_dni = ttk.Entry(tab_personas, font=("verdana", 11))
entry_dni.place(x=90, y=20)

ttk.Label(tab_personas, text="Nombre:", font=("verdana", 11)).place(x=50, y=60)
entry_nombre = ttk.Entry(tab_personas, font=("verdana", 11))
entry_nombre.place(x=120, y=60)

ttk.Label(tab_personas, text="Apellido1:", font=("verdana", 11)).place(x=50, y=100)
entry_ape1 = ttk.Entry(tab_personas, font=("verdana", 11))
entry_ape1.place(x=130, y=100)

ttk.Label(tab_personas, text="Apellido2:", font=("verdana", 11)).place(x=50, y=140)
entry_ape2 = ttk.Entry(tab_personas, font=("verdana", 11))
entry_ape2.place(x=130, y=140)

ttk.Label(tab_personas, text="Fecha Nac. (YYYY-MM-DD):", font=("verdana", 11)).place(x=50, y=180)
entry_fecha = ttk.Entry(tab_personas, font=("verdana", 11))
entry_fecha.place(x=270, y=180)

ttk.Label(tab_personas, text="Ciudad Origen:", font=("verdana", 11)).place(x=50, y=220)
entry_ciudad = ttk.Entry(tab_personas, font=("verdana", 11))
entry_ciudad.place(x=165, y=220)

ttk.Label(tab_personas, text="ID Grupo:", font=("verdana", 11)).place(x=50, y=260)
entry_ciudad = ttk.Entry(tab_personas, font=("verdana", 11))
entry_ciudad.place(x=130, y=260)

btn_agregar = ttk.Button(tab_personas, text="Agregar")
btn_agregar.place(x=50, y=300)

btn_borrar = ttk.Button(tab_personas, text="Borrar")
btn_borrar.place(x=150, y=300)

btn_actualizar = ttk.Button(tab_personas, text="Actualizar")
btn_actualizar.place(x=250, y=300)

btn_buscar = ttk.Button(tab_personas, text="Buscar")
btn_buscar.place(x=350, y=300)

# Treeview para los datos de personas
cols = ("DNI", "Nombre", "Apellido 1", "Apellido 2", "Fecha de nacimiento", "Ciudad de Origen", "Grupo")
tree_personas = ttk.Treeview(tab_personas, columns=cols, show="headings", height=15)


for col in cols:
    tree_personas.heading(col, text=col)
    tree_personas.column(col, width=120)

tree_personas.place(x=600, y=20, width=860, height=500)

# ------------------------------------------------------------------------------------------
#  Gestión de grupo (Grupos numerados y tiempo de viaje,)
# ------------------------------------------------------------------------------------------

tab_grupos = ttk.Frame(notebook)
notebook.add(tab_grupos, text="Grupos")

ttk.Label(tab_grupos, text="ID Grupo:", font=("verdana", 11)).place(x=50, y=20)
entry_id_grupo = ttk.Entry(tab_grupos, font=("verdana", 11))
entry_id_grupo.place(x=130, y=20)

ttk.Label(tab_grupos, text="Número Integrantes:", font=("verdana", 11)).place(x=50, y=60)
entry_num_integrantes = ttk.Entry(tab_grupos, font=("verdana", 11))
entry_num_integrantes.place(x=220, y=60)

ttk.Label(tab_grupos, text="Fecha Inicio (YYYY-MM-DD):", font=("verdana", 11)).place(x=50, y=100)
entry_fecha_inicio = ttk.Entry(tab_grupos, font=("verdana", 11))
entry_fecha_inicio.place(x=270, y=100)

ttk.Label(tab_grupos, text="Fecha Fin (YYYY-MM-DD):", font=("verdana", 11)).place(x=50, y=140)
entry_fecha_fin = ttk.Entry(tab_grupos, font=("verdana", 11))
entry_fecha_fin.place(x=260, y=140)

ttk.Label(tab_grupos, text="Precio:", font=("verdana", 11)).place(x=50, y=180)
entry_fecha_fin = ttk.Entry(tab_grupos, font=("verdana", 11))
entry_fecha_fin.place(x=115, y=180)

ttk.Label(tab_grupos, text="ID Viaje:", font=("verdana", 11)).place(x=50, y=220)
entry_fecha_fin = ttk.Entry(tab_grupos, font=("verdana", 11))
entry_fecha_fin.place(x=125, y=220)

ttk.Label(tab_grupos, text="ID Curso:", font=("verdana", 11)).place(x=50, y=260)
entry_fecha_fin = ttk.Entry(tab_grupos, font=("verdana", 11))
entry_fecha_fin.place(x=125, y=260)

btn_agregar_grupo = ttk.Button(tab_grupos, text="Agregar")
btn_agregar_grupo.place(x=50, y=300)

btn_borrar_grupo = ttk.Button(tab_grupos, text="Borrar")
btn_borrar_grupo.place(x=150, y=300)

btn_actualizar_grupo = ttk.Button(tab_grupos, text="Actualizar")
btn_actualizar_grupo.place(x=250, y=300)

btn_buscar_grupo = ttk.Button(tab_grupos, text="Buscar")
btn_buscar_grupo.place(x=350, y=300)

# Treeview para mostrar datos de los cursos
cols = ("Grupo","Fecha de Inicio", "Fecha de Fin", "Precio","ID Viaje","ID Curso")
tree_grupos = ttk.Treeview(tab_grupos, columns=cols, show="headings", height=20)

for col in cols:
    tree_grupos.heading(col, text=col)
    tree_grupos.column(col, width=120)

tree_grupos.place(x=600, y=20, width=860, height=500)

# ------------------------------------------------------------------------------------------
#  Gestión de ITINERARIOS
# ------------------------------------------------------------------------------------------

tab_itinerario = ttk.Frame(notebook)
notebook.add(tab_itinerario, text="Itinerario")

ttk.Label(tab_itinerario, text="ID Viaje:", font=("verdana", 11)).place(x=30, y=20)
entry_id_grupo = ttk.Entry(tab_itinerario, font=("verdana", 11))
entry_id_grupo.place(x=110, y=20)

ttk.Label(tab_itinerario, text="Ciudad:", font=("verdana", 11)).place(x=30, y=60)
entry_num_integrantes = ttk.Entry(tab_itinerario, font=("verdana", 11))
entry_num_integrantes.place(x=95, y=60)

ttk.Label(tab_itinerario, text="Inicio(YYYY-MM-DD):", font=("verdana", 11)).place(x=30, y=100)
entry_fecha_inicio = ttk.Entry(tab_itinerario, font=("verdana", 11))
entry_fecha_inicio.place(x=190, y=100)

ttk.Label(tab_itinerario, text="Fin(YYYY-MM-DD):", font=("verdana", 11)).place(x=30, y=140)
entry_fecha_fin = ttk.Entry(tab_itinerario, font=("verdana", 11))
entry_fecha_fin.place(x=175, y=140)

ttk.Label(tab_itinerario, text="Tipo curso:", font=("verdana", 11)).place(x=30, y=180)
entry_fecha_fin = ttk.Entry(tab_itinerario, font=("verdana", 11))
entry_fecha_fin.place(x=125, y=180)

ttk.Label(tab_itinerario, text="ID Curso:", font=("verdana", 11)).place(x=30, y=220)
entry_fecha_fin = ttk.Entry(tab_itinerario, font=("verdana", 11))
entry_fecha_fin.place(x=110, y=220)

ttk.Label(tab_itinerario, text="Escuela:", font=("verdana", 11)).place(x=30, y=260)
entry_fecha_fin = ttk.Entry(tab_itinerario, font=("verdana", 11))
entry_fecha_fin.place(x=100, y=260)

btn_agregar_grupo = ttk.Button(tab_itinerario, text="Actualizar")
btn_agregar_grupo.place(x=30, y=300)

btn_borrar_grupo = ttk.Button(tab_itinerario, text="Borrar")
btn_borrar_grupo.place(x=130, y=300)

# Treeview para mostrar datos de los itinerarios
cols = ("Grupo","ID Viaje","Ciudad","Alojamiento","Fecha inicio", "Fecha de Fin", "Tipo de Curso","ID Curso","Escuela")
tree_itinerario = ttk.Treeview(tab_itinerario, columns=cols, show="headings", height=20)

for col in cols:
    tree_itinerario.heading(col, text=col)
    tree_itinerario.column(col, width=120)

tree_itinerario.place(x=400, y=20, width=1110, height=500)

# EJECUCIÓN DEL PROGRAMA
root.mainloop()

#Cierro el cursor y la conexión a la abse de datos
c.close()
db.close()
