# Implementando Python en mi base de datos
import mysql.connector 

# Datos de conexión al servidor MySQL
db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    passwd="josegras",
    database="Gestion de viaje"
)

# Creo un cursor para la base de datos
c = db.cursor()

# ##############################
#FUNCIONES DE INSTANCIACIÓN
# ##############################

# ------------------------------
# ENTIDADES FUERTES
# ------------------------------

# PERSONA
def insertar_persona(DNI, nombre, apellido1, apellido2, fecha_nacimiento, ciudad_origen):

    c.execute("""
        INSERT INTO Persona (DNI, Nombre, Apellido1, Apellido2, `Fecha de nacimiento`, Ciudad_Origen) 
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (DNI, nombre, apellido1, apellido2, fecha_nacimiento, ciudad_origen))

    db.commit()
    print(f"Se ha adicionado a {nombre} {apellido1} en la base de datos")

# GRUPO
def insertar_grupo(identificador_grupo, numero_integrantes):
    c.execute("""
        INSERT INTO Grupo (`Identificador de grupo`, `Numero de integrantes`)
        VALUES (%s, %s)
    """, (identificador_grupo, numero_integrantes))

    db.commit()
    print(f"Se ha añadido el grupo '{identificador_grupo}' con {numero_integrantes} integrantes a la base de datos.")

# DESTINO
def insertar_destino(idDestino, ciudad, alojamiento):
    c.execute("""
        INSERT INTO Destino (idDestino, Ciudad, Alojamiento)
        VALUES (%s, %s, %s)
    """, (idDestino, ciudad, alojamiento))

    db.commit()
    print(f"Se ha añadido el destino '{ciudad}' con ID '{idDestino}'.")

# CURSO 
def insertar_curso(idCurso, tipo, escuela):
    c.execute("""
        INSERT INTO Curso (idCurso, Tipo, Escuela)
        VALUES (%s, %s, %s)
    """, (idCurso, tipo, escuela))

    db.commit()
    print(f"Se ha añadido el curso '{tipo}' en la escuela '{escuela}' con ID '{idCurso}'.")

# ------------------------------
# AGREGACIONES
# ------------------------------

# UBICADO
def insertar_ubicado(idCurso, idDestino, fecha_inicio, fecha_fin):
    c.execute("""
        INSERT INTO ubicado (idCurso, idDestino, `Fecha Inicio Curso`, `Fecha Fin Curso`)
        VALUES (%s, %s, %s, %s)
    """, (idCurso, idDestino, fecha_inicio, fecha_fin))
    
    db.commit()
    print(f"Se ha registrado la ubicación del curso '{idCurso}' en el destino '{idDestino}' desde {fecha_inicio} hasta {fecha_fin}.")



# ------------------------------
# CONEXIONES
# ------------------------------

# VIAJE
def insertar_viaje(precio, fecha_salida, fecha_vuelta, identificador_grupo, idCurso, idDestino):
    c.execute("""
        INSERT INTO viaja (Precio, `Fecha Salida`, `Fecha Vuelta`, `Identificador de grupo`, idCurso, idDestino)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (precio, fecha_salida, fecha_vuelta, identificador_grupo, idCurso, idDestino))

    db.commit()
    print(f"Se ha añadido el viaje para el grupo '{identificador_grupo}' asociado al curso '{idCurso}' y destino '{idDestino}'.")


# PERTENECE
def insertar_pertenece(DNI, identificador_grupo):
    c.execute("""
        INSERT INTO pertenece (DNI, `Identificador de grupo`)
        VALUES (%s, %s)
    """, (DNI, identificador_grupo))

    db.commit()
    print(f"La persona con DNI '{DNI}' ha sido asociada al grupo '{identificador_grupo}'.")


# ##############################
# MAIN PARA TESTEO
# ##############################

# Estaré introduciendo los datos como nuevos tipos de dato, para facilitar el proceso de testing

# ------------------------------
# Ejemplo de Instanciación de PERSONA
# ------------------------------

DNI = "12345678Z"
nombre = "Laura"
apellido1 = "Martínez"
apellido2 = "Gómez"
fecha_nacimiento = "1990-07-15"  # formato YYYY-MM-DD para la lectura de datos en MySQL
ciudad_origen = "Sevilla"

# Llamada a la función para insertar la persona
insertar_persona(DNI, nombre, apellido1, apellido2, fecha_nacimiento, ciudad_origen)

# ------------------------------
# Ejemplo de Instanciación de GRUPO
# ------------------------------

identificador_grupo = "GRP001"
numero_integrantes = 25

# Llamada a la función para insertar el grupo
insertar_grupo(identificador_grupo, numero_integrantes)

# ------------------------------
# Ejemplo de Instanciación de DESTINO
# ------------------------------

idDestino = "DST01" 
ciudad = "Granada"
alojamiento = "Hotel Sierra"

# Llamada a la función para insertar el destino
insertar_destino(idDestino, ciudad, alojamiento)

# ------------------------------
# Ejemplo de Instanciación de CURSO
# ------------------------------

idCurso = "CRS01"
tipo = "Formación profesor"
escuela = "Escuela prueba"

# Llamada a la función para insertar el curso
insertar_curso(idCurso, tipo, escuela)

# ------------------------------
# Ejemplo de Instanciación de UBICADO
# ------------------------------

fecha_inicio = "2025-07-01"
fecha_fin = "2025-07-15"
escuela = "Escuela prueba"
ciudad = "Granada"

# Llamada a la función para insertar la ubicación del curso
insertar_ubicado(idCurso, idDestino, fecha_inicio, fecha_fin)


# ------------------------------
# Ejemplo de Instanciación de VIAJA
# ------------------------------

precio = 450.75
fecha_salida = "2025-06-30"
fecha_vuelta = "2025-07-16"
identificador_grupo = "GRP001"
escuela = "Escuela prueba"
ciudad = "Granada"

# Llamada a la función para insertar el viaje
insertar_viaje(precio, fecha_salida, fecha_vuelta, identificador_grupo, idCurso, idDestino)



# ------------------------------
# Ejemplo de Instanciación de PERTENECE
# ------------------------------

DNI = "12345678Z"
identificador_grupo = "GRP001"

# Llamada a la función para insertar la pertenencia
insertar_pertenece(DNI, identificador_grupo)


# Cierro el cursor y la conexión a la base de datos
c.close()
db.close()