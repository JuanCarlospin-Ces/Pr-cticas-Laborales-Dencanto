# Implementando Python en mi base de datos
import mysql.connector 

# Datos de conexión al servidor MySQL
db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    passwd="josegras"
)

# Creo un cursor para la base de datos
c = db.cursor()

# ##############################
#FUNCIONES DE CREACIÓN GENERAL
# ##############################

def crear_Base_De_Datos():

    # Creo la base de datos si no existe
    c.execute("CREATE SCHEMA IF NOT EXISTS `Gestion de viaje` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        
    print("La base de datos 'Gestion de viaje' se ha creado con suceso, o la misma ya existe.")

        
def crear_Tablas_Base_De_Datos():
        
    # Selecciono la base de datos
    c.execute("USE `Gestion de viaje`")
    
    # Tabla Persona
    c.execute("""
    CREATE TABLE IF NOT EXISTS Persona (
        DNI CHAR(9) NOT NULL CHECK (DNI REGEXP '^[0-9]{8}[A-Z]$'),
        Nombre VARCHAR(47) NOT NULL,
        Apellido1 VARCHAR(47) NOT NULL,
        Apellido2 VARCHAR(47) NOT NULL,
        `Fecha de nacimiento` DATE NOT NULL,
        Ciudad_Origen VARCHAR(47) NOT NULL,
        PRIMARY KEY (DNI)
    )
    """)
    
    # Tabla Grupo
    c.execute("""
    CREATE TABLE IF NOT EXISTS Grupo (
        `Identificador de grupo` VARCHAR(10) NOT NULL,
        `Numero de integrantes` INT,
        PRIMARY KEY (`Identificador de grupo`)
    )
    """)
    
    # Tabla Destino
    c.execute("""
    CREATE TABLE IF NOT EXISTS Destino (
        idDestino VARCHAR(5) NOT NULL,
        Ciudad VARCHAR(47) NOT NULL,
        Alojamiento VARCHAR(47) NOT NULL,
        PRIMARY KEY (idDestino)
    )
    """)
    
    # Tabla Curso
    c.execute("""
    CREATE TABLE IF NOT EXISTS Curso (
        idCurso VARCHAR(5) NOT NULL,
        Tipo VARCHAR(47) NOT NULL,
        Escuela VARCHAR(47) NOT NULL,
        PRIMARY KEY (idCurso)
    )
    """)
    
    # Tabla ubicado
    c.execute("""
    CREATE TABLE IF NOT EXISTS ubicado (

        idCurso VARCHAR(5) NOT NULL,
        idDestino VARCHAR(5) NOT NULL,
        `Fecha Inicio Curso` DATE NOT NULL,
        `Fecha Fin Curso` DATE NOT NULL,
        
        PRIMARY KEY (idCurso, idDestino),

        FOREIGN KEY (idCurso) REFERENCES Curso (idCurso),
        FOREIGN KEY (idDestino) REFERENCES Destino (idDestino)
    )
    """)
    
    # Tabla viaja
    c.execute("""
    CREATE TABLE IF NOT EXISTS viaja (
              
        Precio DECIMAL(10,2) NOT NULL,
        `Fecha Salida` DATE NOT NULL,
        `Fecha Vuelta` DATE NOT NULL,
        `Identificador de grupo` VARCHAR(10) NOT NULL,
        idCurso VARCHAR(5) NOT NULL,
        idDestino VARCHAR(5) NOT NULL,

        PRIMARY KEY(`Fecha Salida`, `Fecha Vuelta`, `Identificador de grupo`,idCurso, idDestino),
        FOREIGN KEY(`Identificador de grupo`) REFERENCES Grupo (`Identificador de grupo`),
        FOREIGN KEY(idCurso, idDestino) REFERENCES ubicado (idCurso, idDestino)
    )
    """)
    
    # Tabla pertenece
    c.execute("""
    CREATE TABLE IF NOT EXISTS pertenece (
        DNI CHAR(9) NOT NULL CHECK (DNI REGEXP '^[0-9]{8}[A-Z]$'),
        `Identificador de grupo` VARCHAR(10) NOT NULL,
        PRIMARY KEY (DNI, `Identificador de grupo`),
        FOREIGN KEY (DNI) REFERENCES Persona (DNI),
        FOREIGN KEY (`Identificador de grupo`) REFERENCES Grupo (`Identificador de grupo`)
    )
    """)
    
    print("Todas las tablas se han creado con éxito, o las mismas ya existen.")
    
    # Mostrar las tablas creadas en terminal

    c.execute("SHOW TABLES")
    print("\nTablas en la base de datos 'Gestion de viaje':")
    for tabla in c:
        print(tabla[0])


# ##############################
# MAIN DEL PROGRAMA
# ##############################

crear_Base_De_Datos()
crear_Tablas_Base_De_Datos()

#Cierro el cursor y la conexión a la abse de datos
c.close()
db.close()