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
# FUNCIONES PARA BORRAR DATOS
# ##############################

# Función para borrar todo el contenido de una tabla pasada como parametro

# Ejemplo: Borrar solo los datos de la tabla Persona
# borrar_contenido_tabla("Persona")

def borrar_contenido_tabla(nombre_tabla):

    c.execute(f"DELETE FROM {nombre_tabla}")
    db.commit()
    print(f"Todos los datos de la tabla '{nombre_tabla}' han sido borrados")


# Función para borrar completamente una tabla pasada como parametro de la base de datos

# Ejemplo: Borrar completamente la tabla Grupo
# borrar_tabla("Grupo")

def borrar_tabla(nombre_tabla):

    # Desactivamos temporalmente las restricciones de clave foránea
    c.execute("SET FOREIGN_KEY_CHECKS = 0")
    
    c.execute(f"DROP TABLE IF EXISTS {nombre_tabla}")
    db.commit()
    
    # Reactivamos las restricciones
    c.execute("SET FOREIGN_KEY_CHECKS = 1")
    
    print(f"La tabla '{nombre_tabla}' ha sido eliminada completamente")


# Función que borra todas las tablas de la base de datos

# Ejemplo: Borrar todas las tablas (reiniciar la base)
# borrar_todas_tablas()

def borrar_todas_tablas():

    # Desactivamos temporalmente las restricciones de clave foránea
    c.execute("SET FOREIGN_KEY_CHECKS = 0")
    
    # Obtenemos lista de todas las tablas
    c.execute("SHOW TABLES")
    tablas = [tabla[0] for tabla in c]
    
    # Borramos cada tabla
    for tabla in tablas:
        c.execute(f"DROP TABLE IF EXISTS {tabla}")
        print(f"Tabla '{tabla}' eliminada")
    
    db.commit()
    
    # Reactivamos las restricciones
    c.execute("SET FOREIGN_KEY_CHECKS = 1")
    
    print("Todas las tablas han sido eliminadas")

    c.execute("SET FOREIGN_KEY_CHECKS = 1")

# Función que borra la base de datos

def borrar_base_datos():
    """Elimina completamente la base de datos"""

    confirmacion = input("¿ESTÁ SEGURO de borrar la BASE DE DATOS COMPLETA? (s/n): ")
    if confirmacion.lower() != 's':
        print("Operación cancelada")
        return
        
    c.execute("SET FOREIGN_KEY_CHECKS = 0")
    c.execute("DROP DATABASE IF EXISTS `Gestion de viaje`")
    db.commit()
    print(" Base de datos eliminada completamente")
    
    # Reconectar sin especificar base de datos
    db.database = None

    c.execute("SET FOREIGN_KEY_CHECKS = 1")


    
# Borra registros específicos de una tabla según una condición

# Ejemplo: borrar_registro("Persona", "DNI = '12345678A'")
# Parametro seria: "(COLUMNA A BORRAR) = (VALOR A BORRAR)"    
def borrar_registro(tabla, parametro):

    query = f"DELETE FROM {tabla} WHERE {parametro}"
    c.execute(query)
    db.commit()
    print(f"Registro(s) eliminado(s) de '{tabla}' donde {parametro}")
    print(f"Filas afectadas: {c.rowcount}")


    
# ##############################
# MAIN DEL PROGRAMA
# ##############################


# Mostrar menú de opciones, utilizado para el testeo de las funciones

print("\nOpciones de borrado:")
print("1. Borrar contenido de una tabla")
print("2. Borrar una tabla completamente")
print("3. Borrar todas las tablas")
print("4. BORRAR TODA LA BASE DE DATOS(SOLAMENTE PARA TESTEO DE LA FUNCIÓN)")
print("5. Borrar elemento de una tabla")

opcion = input("\nSeleccione una opción (1-5): ")

if opcion == "1":
    tabla = input("Ingrese el nombre de la tabla a vaciar: ")
    borrar_contenido_tabla(tabla)

elif opcion == "2":
    tabla = input("Ingrese el nombre de la tabla a eliminar: ")
    borrar_tabla(tabla)

elif opcion == "3":
    confirmacion = input("¿Está seguro de borrar TODAS las tablas? (s/n): ")
    if confirmacion.lower() == "s":
        borrar_todas_tablas()

elif opcion == "4":
    confirmacion = input("¿Está seguro de borrar TODA la base de datos? (s/n): ")
    if confirmacion.lower() == "s":
        borrar_base_datos()

elif opcion == "5":
    tabla = input("Ingrese nombre de la tabla: ")
    columna = input("Ingrese columna para condición (ej: DNI): ")
    valor = input(f"Ingrese valor de {columna} a borrar: ")
    parametro = f"{columna} = '{valor}'" 
    borrar_registro(tabla, parametro)
    
else:
    print("Opción no válida")

# Cierro el cursor y la conexión a la base de datos
c.close()
db.close()