import tkinter as tk #Le agrego el alias tk a las funciones importadas de la biblioteca tkinter
from tkinter import ttk, messagebox
from PIL import Image, ImageTk  # Viene de la librería Pillow, la cual estaré utilizando para añadir el logo de la empresa a la aplicación
import mysql.connector


# Me conecto a la base de datos
db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    passwd="josegras",
    database="Gestion de viaje"
)

# Creo un cursor para la base de datos
c = db.cursor()


# ################################
# FUNCIONES
# ################################


#   @brief Carga los datos de la tabla Persona y los muestra en el treeview correspondiente.
#   @return Los respectivos datos de la entidad PERSONA, en la pestaña :
#
#    - DNI
#    - Nombre
#    - Apellido1
#    - Apellido2
#    - Fecha de nacimiento
#    - Ciudad de Origen
#    - Identificador de grupo (o 'Sin grupo' si no pertenece a ninguno)
def cargar_personas():

    
    # Limpio el treeview primero
    for item in tree_personas.get_children():
        tree_personas.delete(item)
    
    # Consulto la base de datos
    c.execute("""
        SELECT p.DNI, p.Nombre, p.Apellido1, p.Apellido2, p.`Fecha de nacimiento`, p.Ciudad_Origen, 
               IFNULL(pe.`Identificador de grupo`, 'Sin grupo')
        FROM Persona p
        LEFT JOIN pertenece pe ON p.DNI = pe.DNI
    """)
    personas = c.fetchall()
    
    # Insertar los datos en el treeview
    for persona in personas:
        tree_personas.insert("", "end", values=persona)


#   @brief Carga los datos de la tabla Grupo y los muestra en el treeview correspondiente.
#   @return Los respectivos datos de la entidad GRUPO, en la pestaña:
#
#    - Identificador de grupo
#    - Número de integrantes
#    - Fecha de inicio mínima del viaje del grupo
#    - Fecha de fin máxima del viaje del grupo
#    - Suma total del precio de los viajes del grupo
#    - Cantidad de cursos distintos
#    - Cantidad de destinos distintos
def cargar_grupos():
    
    # Limpio el treeview primero
    for item in tree_grupos.get_children():
        tree_grupos.delete(item)
    
    # Consulto la base de datos - MODIFICADO para incluir Numero de integrantes
    c.execute("""
        SELECT g.`Identificador de grupo`, 
               g.`Numero de integrantes`,
               MIN(v.`Fecha Salida`), MAX(v.`Fecha Vuelta`), 
               SUM(v.Precio), COUNT(DISTINCT v.idCurso), COUNT(DISTINCT v.idDestino)
        FROM Grupo g
        LEFT JOIN viaja v ON g.`Identificador de grupo` = v.`Identificador de grupo`
        GROUP BY g.`Identificador de grupo`, g.`Numero de integrantes`
    """)
    grupos = c.fetchall()
    
    # Insertar los datos en el treeview
    for grupo in grupos:
        tree_grupos.insert("", "end", values=grupo)

#   @brief Carga los datos del itinerario y los muestra en el treeview correspondiente.
#   @return Los datos combinados de la entidad VIAJA junto con información de DESTINO y CURSO, en la pestaña:
#
#    - Identificador de grupo
#    - Identificador del viaje (concatenación de idCurso e idDestino)
#    - Ciudad del destino
#    - Alojamiento del destino
#    - Fecha de salida
#    - Fecha de vuelta
#    - Tipo de curso
#    - Identificador de curso
#    - Escuela que imparte el curso
def cargar_itinerario():
    # Limpiar el treeview primero
    for item in tree_itinerario.get_children():
        tree_itinerario.delete(item)
    
    # Consultar la base de datos
    c.execute("""
        SELECT v.`Identificador de grupo`, 
               CONCAT(v.idCurso, '-', v.idDestino) as ID_Viaje,
               d.Ciudad, d.Alojamiento,
               v.`Fecha Salida`, v.`Fecha Vuelta`,
               c.Tipo, c.idCurso, c.Escuela
        FROM viaja v
              
        JOIN Destino d ON v.idDestino = d.idDestino
        JOIN Curso c ON v.idCurso = c.idCurso
        ORDER BY v.`Fecha Salida`
    """)
    itinerarios = c.fetchall()
    
    # Insertar los datos en el treeview
    for itinerario in itinerarios:
        tree_itinerario.insert("", "end", values=itinerario)

#   @brief Inserta una nueva persona en la base de datos, vinculándola con un grupo si el mismo existe de antemano.
#   Esta función recoge los datos introducidos en los campos de entrada del formulario
#   en la pestaña de "Personas" y realiza las siguientes acciones:
#
#        - Verifica que todos los campos obligatorios estén completos.
#        - Inserta los datos en la tabla Persona.
#        - Si se proporciona un ID de grupo:
#             - Verifica si ese grupo ya existe en la tabla Grupo.
#             - Si no existe, lo crea automáticamente con el identificador dado.
#             - Luego, vincula la persona al grupo insertando en la tabla pertenece.

#         - Actualiza visualmente el treeview de personas.
#
#   @return Muestra una ventana emergente informando si la operación fue exitosa o si faltan campos.

def agregar_persona():
    
    #Datos persona
    DNI = entry_dni.get()
    nombre = entry_nombre.get()
    apellido1 = entry_ape1.get()
    apellido2 = entry_ape2.get()
    fecha_nacimiento = entry_fecha.get()
    ciudad_origen = entry_ciudad.get()

    id_grupo = entry_grupo.get()
    
    # Verifico que todos los campos están completos
    if not (DNI and nombre and apellido1 and apellido2 and fecha_nacimiento and ciudad_origen):
        messagebox.showinfo("ALERTA", "Por favor, complete todos los campos")
        return
    
    c.execute("""
            INSERT INTO Persona (DNI, Nombre, Apellido1, Apellido2, `Fecha de nacimiento`, Ciudad_Origen)
            VALUES (%s, %s, %s, %s, %s, %s)""",(DNI, nombre, apellido1, apellido2, fecha_nacimiento, ciudad_origen))
    
    if id_grupo:
    # Verifico si el grupo existe
        c.execute("SELECT COUNT(*) FROM Grupo WHERE `Identificador de grupo` = %s", (id_grupo,))
        existe = c.fetchone()[0]

        # En el caso que no exista, lo creo con datos mínimos por defecto

        if not existe:
            c.execute("""
                INSERT INTO Grupo (`Identificador de grupo`) 
                VALUES (%s)
            """, (id_grupo,))
        
        # Insertao el grupo en pertenece
        c.execute("INSERT INTO pertenece (DNI, `Identificador de grupo`) VALUES (%s, %s)", (DNI, id_grupo))
    
    db.commit()
    
    cargar_personas()
    messagebox.showinfo("Estado", "Persona agregada con éxito")

#   FUNCION EN DESAROLLO - ESTADO NO FUNCIONAL
#   @brief Inserta un nuevo grupo en la base de datos, junto con los datos asociados al viaje.
#   Esta función recoge los datos introducidos en los campos de entrada del formulario
#   en la pestaña de "Grupos" y realiza las siguientes acciones:
#
#        - Verifica que todos los campos estén completos.
#        - Inserta el grupo en la tabla Grupo (si aún no existe).
#        - Inserta el viaje en la tabla viaja, conectando grupo, curso y destino, junto con fechas y precio.
#        - Actualiza visualmente el treeview de grupos.
#
#   @return Muestra una ventana emergente informando si la operación fue exitosa o si faltan campos.
def agregar_grupo():

    id_grupo = entry_id_grupo.get()
    num_integrantes = entry_num_integrantes.get()
    fecha_inicio = entry_fecha_inicio.get()
    fecha_fin = entry_fecha_fin.get()
    precio = entry_precio.get()
    id_destino = entry_idViaje.get() 
    id_curso = entry_idCurso.get()

    # DEBUG

    print("id_grupo:", id_grupo)
    print("fecha_inicio:", fecha_inicio)
    print("fecha_fin:", fecha_fin)
    print("id_curso:", id_curso)
    print("id_destino:", id_destino)


    # Validar campos obligatorios
    if not (id_grupo and fecha_inicio and fecha_fin and id_curso and id_destino):
        messagebox.showinfo("ALERTA", "Por favor, complete todos los campos obligatorios.")
        return


    # Insertar grupo si no existe
    c.execute("SELECT COUNT(*) FROM Grupo WHERE `Identificador de grupo` = %s", (id_grupo,))
    if c.fetchone()[0] == 0:
        c.execute("INSERT INTO Grupo (`Identificador de grupo`,`Numero de integrantes`) VALUES (%s, %s)", (id_grupo,num_integrantes))

    # Verificar si el valores de curso existen en la tabla Curso

    c.execute("SELECT COUNT(*) FROM curso WHERE idCurso = %s", (id_curso,))
    existe = c.fetchone()[0]
    
    if not existe:
        # Crear automáticamente Curso con el id
        c.execute("""
            INSERT INTO curso (idCurso)
            VALUES (%s)
        """, (id_curso,))

    # Verificar si el valores de destino existen en la tabla Destino
    
    c.execute("SELECT COUNT(*) FROM destino WHERE idDestino = %s", (id_destino,))
    existe_destino = c.fetchone()[0]
    
    if not existe_destino:
        # Crear automáticamente Destino con el id
        c.execute("""
            INSERT INTO destino (idDestino)
            VALUES (%s)
        """, (id_destino,))

    # Verificar si los valores de curso y destino existen en la tabla ubicado
    c.execute("SELECT COUNT(*) FROM ubicado WHERE idCurso = %s AND idDestino = %s", (id_curso, id_destino))
    existe = c.fetchone()[0]
    
    if not existe:
        # Crear automáticamente con las fechas insertadas
        c.execute("""
            INSERT INTO ubicado (idCurso, idDestino, `Fecha Inicio Curso`, `Fecha Fin Curso`)
            VALUES (%s, %s, %s, %s)
        """, (id_curso, id_destino, fecha_inicio, fecha_fin))

    # Insertar viaje en tabla viaja
    c.execute("""
        INSERT INTO viaja (`Identificador de grupo`, idCurso, idDestino, `Fecha Salida`, `Fecha Vuelta`, Precio)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (id_grupo, id_curso, id_destino, fecha_inicio, fecha_fin, precio))

    db.commit()
    cargar_grupos()
    messagebox.showinfo("Estado", "Grupo y viaje agregado con éxito.")



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
entry_grupo = ttk.Entry(tab_personas, font=("verdana", 11))
entry_grupo.place(x=130, y=260)

# BOTONES

btn_agregar = ttk.Button(tab_personas, text="Agregar", command=agregar_persona)
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
entry_precio = ttk.Entry(tab_grupos, font=("verdana", 11))
entry_precio.place(x=115, y=180)

ttk.Label(tab_grupos, text="ID Viaje:", font=("verdana", 11)).place(x=50, y=220)
entry_idViaje = ttk.Entry(tab_grupos, font=("verdana", 11))
entry_idViaje.place(x=125, y=220)

ttk.Label(tab_grupos, text="ID Curso:", font=("verdana", 11)).place(x=50, y=260)
entry_idCurso = ttk.Entry(tab_grupos, font=("verdana", 11))
entry_idCurso.place(x=125, y=260)

# BOTONES

btn_agregar_grupo = ttk.Button(tab_grupos, text="Agregar",command=agregar_grupo)
btn_agregar_grupo.place(x=50, y=300)

btn_borrar_grupo = ttk.Button(tab_grupos, text="Borrar")
btn_borrar_grupo.place(x=150, y=300)

btn_actualizar_grupo = ttk.Button(tab_grupos, text="Actualizar")
btn_actualizar_grupo.place(x=250, y=300)

btn_buscar_grupo = ttk.Button(tab_grupos, text="Buscar")
btn_buscar_grupo.place(x=350, y=300)

# Treeview para mostrar datos de los grupos
cols = ("Grupo","Número de integrantes","Fecha de Inicio", "Fecha de Fin", "Precio","ID Viaje","ID Curso")
tree_grupos = ttk.Treeview(tab_grupos, columns=cols, show="headings", height=20)

for col in cols:
    tree_grupos.heading(col, text=col)
    tree_grupos.column(col, width=120)

tree_grupos.place(x=590, y=20, width=910, height=500)

# ------------------------------------------------------------------------------------------
#  Gestión de ITINERARIOS
# ------------------------------------------------------------------------------------------

tab_itinerario = ttk.Frame(notebook)
notebook.add(tab_itinerario, text="Itinerario")

ttk.Label(tab_itinerario, text="ID Viaje:", font=("verdana", 11)).place(x=30, y=20)
entry_id_grupo_Itinerario = ttk.Entry(tab_itinerario, font=("verdana", 11))
entry_id_grupo_Itinerario.place(x=110, y=20)

ttk.Label(tab_itinerario, text="Ciudad:", font=("verdana", 11)).place(x=30, y=60)
entry_ciudad_itinerario = ttk.Entry(tab_itinerario, font=("verdana", 11))
entry_ciudad_itinerario.place(x=95, y=60)

ttk.Label(tab_itinerario, text="Inicio(YYYY-MM-DD):", font=("verdana", 11)).place(x=30, y=100)
entry_fecha_inicio_Itinerario = ttk.Entry(tab_itinerario, font=("verdana", 11))
entry_fecha_inicio_Itinerario.place(x=190, y=100)

ttk.Label(tab_itinerario, text="Fin(YYYY-MM-DD):", font=("verdana", 11)).place(x=30, y=140)
entry_fecha_fin_Itinerario = ttk.Entry(tab_itinerario, font=("verdana", 11))
entry_fecha_fin_Itinerario.place(x=175, y=140)

ttk.Label(tab_itinerario, text="Tipo curso:", font=("verdana", 11)).place(x=30, y=180)
entry_curso = ttk.Entry(tab_itinerario, font=("verdana", 11))
entry_curso.place(x=125, y=180)

ttk.Label(tab_itinerario, text="ID Curso:", font=("verdana", 11)).place(x=30, y=220)
entry_idCurso_Itinerario = ttk.Entry(tab_itinerario, font=("verdana", 11))
entry_idCurso_Itinerario.place(x=110, y=220)

ttk.Label(tab_itinerario, text="Escuela:", font=("verdana", 11)).place(x=30, y=260)
entry_Escuela = ttk.Entry(tab_itinerario, font=("verdana", 11))
entry_Escuela.place(x=100, y=260)

# BOTONES

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
cargar_grupos()
cargar_itinerario()
cargar_personas()
root.mainloop()

#Cierro el cursor y la conexión a la abse de datos
c.close()
db.close()
