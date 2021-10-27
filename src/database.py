import sqlite3 as sql

def crearDB():
    conexion = sql.connect("nonces.db")
    conexion.commit()
    conexion.close()

# User TEXT /// Nonce INTEGER
def crearTabla():
    conexion = sql.connect("nonces.db")
    cursor = conexion.cursor()
    cursor.execute("""CREATE TABLE nonces (
                    nonce text
                    )""")
    conexion.commit()
    conexion.close()

def insertarUser(user,password,clave,nonce):
    conexion = sql.connect("nonces.db")
    cursor = conexion.cursor()
    ins = f"INSERT INTO nonces VALUES ('{user}','{password}','{clave}','{nonce}')"
    cursor.execute(ins)
    conexion.commit()
    conexion.close()

def updateClave(user,nuevoClave):
    conexion = sql.connect("nonces.db")
    cursor = conexion.cursor()
    ins = f"UPDATE nonces SET clave={nuevoClave} WHERE user like '{user}'"
    cursor.execute(ins)
    conexion.commit()
    conexion.close()

#crearDB()
#crearTabla()
insertarUser('Antonio Parra','3k2r','apd',2723443)
insertarUser('Juan Alberto','59405','j2000X',490033)
insertarUser('Antonio Lopez','eifki240','alpALP10',9409554)
#updateUser('Juan Alberto',10)