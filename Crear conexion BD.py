# Implementando Python en mi base de datos
import mysql.connector 

# Datos de conexión al servidor
db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    passwd="josegras"
)

#  Creo el cursor para la base de datos
c = db.cursor()

# Recogo la base de datos
c.execute("SHOW DATABASES")

# Imprimo todas las bases de datos
for i in c:
    print(i)
c = db.cursor()

# Cierro la conexión a la base de datos
db.close()