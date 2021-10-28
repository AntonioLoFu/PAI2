import socket, hmac, hashlib
from log import *
from database import *
from diffieHellman import *
from kpi import *

HOST = "0.0.0.0" #CON ESTA IP PODEMOS ACCEDER DESDE LA RED LOCAL Y DESDE EL EQUIPO
PORT = 10000
LONGITUD = 1024
FORMATO = "utf-8"

ALGORITMOS_POSIBLES = ['sha224', 'sha256', 'sha1', 'md5']

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

    #GENERAMOS LA CLAVE PRIVADA DEL SERVIDOR
    serverPrivateKey = generaPrimoAleatorio(1, 100)

    #GENERAMOS Y ENVIAMOS UNA CLAVE PÚBLICA 
    serverPublicKey = generaPrimoAleatorio(1, 100)
    conn.sendall(str(serverPublicKey).encode(FORMATO))

    #RECIBIMOS LA CLAVE PÚBLICA DEL CLIENTE
    clientPublicKey = conn.recv(LONGITUD).decode(FORMATO)

    #CREAMOS UNA INSTANCIA DE LA CLASE DIFFIE-HELLMAN CON LAS CLAVES CORRESPONDIENTES
    diffie = DH(serverPublicKey, int(clientPublicKey), serverPrivateKey)
    
    #ENVIAMOS NUESTRA CLAVE PARCIAL
    conn.sendall(str(diffie.calculaParcial()).encode(FORMATO))

    #Y RECIBIMOS LA PARCIAL DEL CLIENTE
    clienteParcial = conn.recv(LONGITUD).decode(FORMATO)

    conn.sendall(b"TRANSMISION DE CLAVES COMPLETA")

    print("Nueva conexion con: " + str(direccion))

    #RECIBIMOS EL ALGORITMO DE CODIFICACION POR PARTE DEL CLIENTE Y COMPROBAMOS SI HA ELEGIDO UNO DE ENTRE LOS DISPONIBLES
    algoritmo = conn.recv(LONGITUD).decode(FORMATO)
    if algoritmo not in ALGORITMOS_POSIBLES:
        conn.sendall(b"EL ALGORITMO ESCOGIDO NO ES CORRECTO, ABORTANDO CONEXION")
        conn.close()
        return


    conn.sendall(b"ALGORITMO ADECUADO, PROCEDIENDO A VALIDAR LA TRANSACCION")

    #RECIBIMOS EL (MENSAJE, NONCE) DE LA TRANSACCION CON SU MAC 
    mensaje, macMensaje = conn.recv(LONGITUD).decode(FORMATO).rsplit(' ', 1)

    #CALCULAMOS LA CLAVE FINAL CON LA CLAVE PARCIAL DEL CLIENTE
    claveFinal = str(diffie.calculaFinal(int(clienteParcial))).encode(FORMATO)

    #CALCULAMOS LA MAC DEL MENSAJE PARA LUEGO COMPROBAR SU INTEGRIDAD Y SACAMOS EL NONCE
    macMensajeCalculado = hmac.new(key = claveFinal, msg = mensaje.encode(FORMATO), digestmod = algoritmo)
    nonce = mensaje.rsplit(' ', 1)[1]

    #SI EL NONCE NO ESTÁ EN LA BASE DE DATOS Y LA MAC DEL MENSAJE COINCIDE CON LA CALCULADA LA TRANSACCIÓN ES EXITOSA
    if nonceExistente(nonce):
        conn.sendall(b"LA OPERACION NO SE HA PODIDO REALIZAR POR NONCE REPETIDO")
        creaLog(mensaje, False)
    else:
        insertarNonce(nonce)
        if macMensajeCalculado.hexdigest() == macMensaje:
            creaLog(mensaje, True)
            conn.sendall(b"LA OPERACION SE HA REALIZADO CORRECTAMENTE")
            print(KPI())
        else:
            creaLog(mensaje, False)
            conn.sendall(b"LA OPERACION NO SE HA PODIDO REALIZAR YA QUE EL MENSAJE HA SIDO MODIFICADO")
            print(KPI())
            
    conn.close()

arrancar_servidor()