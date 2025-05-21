import mysql.connector

# Conexión a la base de datos
db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="josegras",
    database="Gestion de viaje"
)

# Creo un cursor para la base de datos
c = db.cursor()

# ------------------------------------------
# FUNCIONES PARA VISUALIZAR CADA TABLA
# ------------------------------------------

# PERSONA
def ver_persona():
    c.execute("SELECT * FROM Persona")
    datos = c.fetchall()
    print("\n--- Tabla PERSONA ---")
    for fila in datos:
        print(fila)

# GRUPOS
def ver_grupo():
    c.execute("SELECT * FROM Grupo")
    datos = c.fetchall()
    print("\n--- Tabla GRUPO ---")
    for fila in datos:
        print(fila)

# DESTINO
def ver_destino():
    c.execute("SELECT * FROM Destino")
    datos = c.fetchall()
    print("\n--- Tabla DESTINO ---")
    for fila in datos:
        print(fila)

# CURSOS
def ver_curso():
    c.execute("SELECT * FROM Curso")
    datos = c.fetchall()
    print("\n--- Tabla CURSO ---")
    for fila in datos:
        print(fila)

# UBICADO
def ver_ubicacion():
    c.execute("SELECT * FROM ubicado")
    datos = c.fetchall()
    print("\n--- Tabla UBICADO ---")
    for fila in datos:
        print(fila)

# VIAJA
def ver_viaje():
    c.execute("SELECT * FROM viaja")
    datos = c.fetchall()
    print("\n--- Tabla VIAJA ---")
    for fila in datos:
        print(fila)

# PERTENECE
def ver_pertenence():
    c.execute("SELECT * FROM pertenece")
    datos = c.fetchall()
    print("\n--- Tabla PERTENECE ---")
    for fila in datos:
        print(fila)

# ------------------------------------------
# LLAMADAS DE PRUEBA PARA VER TODAS LAS TABLAS
# ------------------------------------------

ver_persona()
ver_grupo()
ver_destino()
ver_curso()
ver_ubicacion()
ver_viaje()
ver_pertenence()

# Cierre de conexión
c.close()
db.close()
