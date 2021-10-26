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
                    user text,
                    nonce integer
                    )""")
    conexion.commit()
    conexion.close()

def insertarUser(user,nonce):
    conexion = sql.connect("nonces.db")
    cursor = conexion.cursor()
    ins = f"INSERT INTO nonces VALUES ('{user}',{nonce})"
    cursor.execute(ins)
    conexion.commit()
    conexion.close()

def updateUser(user,nuevoNonce):
    conexion = sql.connect("nonces.db")
    cursor = conexion.cursor()
    ins = f"UPDATE nonces SET nonce={nuevoNonce} WHERE user like '{user}'"
    cursor.execute(ins)
    conexion.commit()
    conexion.close()

#crearDB()
#crearTabla()
#insertarUser('Antonio Parra',2723443)
#insertarUser('Juan Alberto',490033)
#insertarUser('Antonio Lopez',9409554)
#updateUser('Juan Alberto',10)