import sqlite3 as sql

def crearDB():
    conexion = sql.connect("nonces.db")
    conexion.commit()
    conexion.close()

# User TEXT /// Nonce INTEGER
def crearTabla():
    conexion = sql.connect("nonces.db")
    cursor = conexion.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS nonces (
                    nonce text
                    )""")
    conexion.commit()
    conexion.close()

def insertarNonce(nonce):
    conexion = sql.connect("nonces.db")
    cursor = conexion.cursor()
    ins = f"INSERT INTO nonces VALUES ('{nonce}')"
    cursor.execute(ins)
    conexion.commit()
    conexion.close()

def nonceExistente(nonce):
    conexion = sql.connect("nonces.db")
    cursor = conexion.cursor()
    ins = f"SELECT * FROM nonces where nonces.nonce = '{nonce}'"
    cursor.execute(ins)
    
    return bool(cursor.fetchone())
    conexion.close()
