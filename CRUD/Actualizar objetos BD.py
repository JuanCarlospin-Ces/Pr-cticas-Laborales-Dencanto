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

# LIMPIO LA BASE DE DATOS, SOLO PARA TESTING
c.execute("DELETE FROM pertenece")
c.execute("DELETE FROM viaja")
c.execute("DELETE FROM ubicado")
c.execute("DELETE FROM Curso")
c.execute("DELETE FROM Destino")
c.execute("DELETE FROM Grupo")
c.execute("DELETE FROM Persona")
db.commit()

# ------------------------------
# Personas
# ------------------------------
insertar_persona("99988877L", "Laura", "López", "García", "1992-04-10", "Madrid")
insertar_persona("31415926K", "Sara", "Alonso", "Muñoz", "1993-03-14", "Granada") 
insertar_persona("11223344A", "Sofía", "Morales", "López", "1993-05-12", "Alicante")
insertar_persona("22334455B", "Luis", "García", "Martín", "1989-11-23", "Sevilla")
insertar_persona("33445566C", "Elena", "Sánchez", "Pérez", "1990-07-08", "Madrid")
insertar_persona("44556677D", "Carlos", "Díaz", "Fernández", "1985-02-17", "Valencia")
insertar_persona("55667788E", "María", "Romero", "Gómez", "1992-09-30", "Granada")
insertar_persona("66778899F", "Javier", "Navarro", "Ruiz", "1987-12-05", "Málaga")
insertar_persona("77889900G", "Lucía", "Torres", "Serrano", "1991-03-14", "Salamanca")
insertar_persona("88990011H", "Miguel", "Vázquez", "Castro", "1988-06-21", "San Sebastián")

# ------------------------------
# Grupos
# ------------------------------
insertar_grupo("GRP001", 2)  
insertar_grupo("GRP005", 4)
insertar_grupo("GRP006", 4)

# ------------------------------
# Destinos
# ------------------------------
insertar_destino("DST01", "Granada", "Hotel Sierra")  
insertar_destino("DST05", "Sevilla", "Hostal Sevilla Centro")
insertar_destino("DST06", "Madrid", "Hotel Madrid Centro")

# ------------------------------
# Cursos
# ------------------------------
insertar_curso("CRS01", "Formación profesor", "Enforex Granada")  
insertar_curso("CRS05", "Curso de formación ELE", "CLIC IH Sevilla")
insertar_curso("CRS06", "Curso intensivo de español + Escalada", "Escuela Montalbán Granada")

# ------------------------------
# Ubicados
# ------------------------------
insertar_ubicado("CRS01", "DST01", "2025-07-01", "2025-07-15")  
insertar_ubicado("CRS05", "DST05", "2025-08-01", "2025-08-15")
insertar_ubicado("CRS06", "DST06", "2025-09-01", "2025-09-15")

# ------------------------------
# Viajes
# ------------------------------
insertar_viaje(450.75, "2025-06-30", "2025-07-16", "GRP001", "CRS01", "DST01")
insertar_viaje(620.00, "2025-10-01", "2025-10-17", "GRP001", "CRS05", "DST05")  # Segundo viaje de GRP001
insertar_viaje(650.00, "2025-07-30", "2025-08-16", "GRP005", "CRS05", "DST05")
insertar_viaje(700.00, "2025-08-30", "2025-09-16", "GRP006", "CRS06", "DST06")

# ------------------------------
# Pertenencias
# ------------------------------
insertar_pertenece("31415926K", "GRP001")
insertar_pertenece("99988877L", "GRP001")

insertar_pertenece("11223344A", "GRP005")
insertar_pertenece("22334455B", "GRP005")
insertar_pertenece("33445566C", "GRP005")
insertar_pertenece("44556677D", "GRP005")

insertar_pertenece("55667788E", "GRP006")
insertar_pertenece("66778899F", "GRP006")
insertar_pertenece("77889900G", "GRP006")
insertar_pertenece("88990011H", "GRP006")



# Cierro el cursor y la conexión a la base de datos
c.close()
db.close()