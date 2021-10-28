import socket
import hashlib
import hmac
from log import *
from database import *
from diffieHellman import *

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


#Intercambio de contraseñas

'''

def handShake(conn):
    clientPublicKey = conn.recv(LONGITUD).decode(FORMATO)
    serverPublicKey = generaPrimoAleatorio(1, 100)
    conn.sendall(str(serverPublicKey).encode(FORMATO))
    serverPrivateKey = generaPrimoAleatorio(1, 100)
    diffie = DH(serverPublicKey, int(clientPublicKey), serverPrivateKey)
    serverPublicKey = diffie.publica1
    conn.sendall(str(serverPublicKey).encode(FORMATO))
    #conn.close()
    return diffie

    '''



#LOGICA DEL SERVIDOR
def manejar_cliente(conn, direccion):
    #RECIBIMOS LA CLAVE PÚBLICA DEL CLIENTE
    clientPublicKey = conn.recv(LONGITUD).decode(FORMATO)
    print("Clave publica del cliente" + str(clientPublicKey))
    #GENERAMOS Y ENVIAMOS UNA CLAVE PÚBLICA 
    serverPublicKey = generaPrimoAleatorio(1, 100)
    conn.sendall(str(serverPublicKey).encode(FORMATO))

    #GENERAMOS LA CLAVE PRIVADA DEL SERVIDOR
    serverPrivateKey = generaPrimoAleatorio(1, 100)
    print("Clave privada del servidor" + str(serverPrivateKey))
    diffie = DH(publica1 = serverPublicKey, publica2 = int(clientPublicKey), privada = serverPrivateKey)
    
    conn.sendall(str(diffie.calculaParcial()).encode(FORMATO))
    print("clave parcial del servidor" + str(diffie.calculaParcial()))
    clienteParcial = conn.recv(LONGITUD).decode(FORMATO)
    print("clave parcial del cliente recibida por el servidor" + str(clienteParcial))
    conn.sendall(b"TRANSMISION DE CLAVES COMPLETA")


    print("Nueva conexion con: " + str(direccion))
    algoritmo = conn.recv(LONGITUD).decode(FORMATO)
    if algoritmo not in hashlib.algorithms_guaranteed:
        conn.sendall(b"EL ALGORITMO ESCOGIDO NO ES CORRECTO, ABORTANDO CONEXION")
        conn.close()
        return
    conn.sendall(b"ALGORITMO ADECUADO, PROCEDIENDO A VALIDAR LA TRANSACCION")
    mensaje, macMensaje = conn.recv(LONGITUD).decode(FORMATO).rsplit(' ', 1)
    claveFinal = str(diffie.calculaFinal(int(clienteParcial))).encode(FORMATO)
    print(claveFinal)
    macMensajeCalculado = hmac.new(key = claveFinal, msg = mensaje.encode(FORMATO), digestmod = algoritmo)
    nonce = mensaje.rsplit(' ', 1)[1]
    if nonceExistente(nonce):
        print(b"LA OPERACION NO SE HA PODIDO REALIZAR POR NONCE REPETIDO")
        creaLog(mensaje, False)
    else:
        insertarNonce(nonce)
        if macMensajeCalculado.hexdigest() == macMensaje:
            creaLog(mensaje, True)
            conn.sendall(b"LA OPERACION SE HA REALIZADO CORRECTAMENTE")
        else:
            print("LA OPERACION NO SE HA PODIDO REALIZAR YA QUE EL MENSAJE HA SIDO MODIFICADO")
            creaLog(mensaje, False)

    conn.close()

arrancar_servidor()