import socket
import hashlib
import hmac
from log import *
from database import *

HOST = "0.0.0.0" #CON ESTA IP PODEMOS ACCEDER DESDE LA RED LOCAL Y DESDE EL EQUIPO
PORT = 10000
LONGITUD = 1024
FORMATO = "utf-8"
CERRAR_CONEXION = "close_connection"
FALLO_VERIFICACION = "123"
CLAVE_CLIENTE = "clave_a_definir"
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))


#ARRANCAMOS EL SERVIDOR Y ACEPTAMOS LAS CONEXIONES ENTRANTES, SOLO UN CLIENTE SIMULTANEAMENTE
def arrancar_servidor():
    crearDB()
    crearTabla()
    server.listen()
    while True:
        conn, direccion = server.accept()
        manejar_cliente(conn, direccion)




#LOGICA DEL SERVIDOR
def manejar_cliente(conn, direccion):
    print("Nueva conexion con: " + str(direccion))
    algoritmo = conn.recv(LONGITUD).decode(FORMATO)
    if algoritmo not in hashlib.algorithms_guaranteed:
        conn.sendall(b"EL ALGORITMO ESCOGIDO NO ES CORRECTO, ABORTANDO CONEXION")
        conn.close()
        return
    conn.sendall(b"ALGORITMO ADECUADO, PROCEDIENDO A VALIDAR LA TRANSACCION")
    mensaje, macMensaje = conn.recv(LONGITUD).decode(FORMATO).rsplit(' ', 1)
    
    macMensajeCalculado = hmac.new(key = CLAVE_CLIENTE.encode(FORMATO), msg = mensaje.encode(FORMATO), digestmod = algoritmo)
    nonce = mensaje.rsplit(' ', 1)[1]
    print(nonce)
    if nonceExistente(nonce):
        print(b"LA OPERACION NO SE HA PODIDO REALIZAR POR NONCE REPETIDO")
        creaLog(mensaje, False)
    else:
        insertarNonce(nonce)
        if macMensajeCalculado.hexdigest() == macMensaje:
            creaLog(mensaje, True)
            conn.sendall(b"LA OPERACION SE HA REALIZADO CORRECTAMENTE")
        else:
            print(b"LA OPERACION NO SE HA PODIDO REALIZAR YA QUE EL MENSAJE HA SIDO MODIFICADO")
            creaLog(mensaje, False)

    conn.close()

arrancar_servidor()