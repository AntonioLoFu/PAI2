import socket
import hashlib
import hmac
HOST = "127.0.0.1"
PORT = 65432
LONGITUD = 1024
FORMATO = "utf-8"
CERRAR_CONEXION = "close_connection"
FALLO_VERIFICACION = "123"
CLAVE_CLIENTE = "clave_a_definir"
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

#PROTOCOLO DE ENVIO DE DATOS AL SERVIDOR, PRIMERO SE INDICA EL NUMERO DE BYTES Y LUEGO SE MANDA EL MENSAJE COMO TAL


#ARRANCAMOS EL SERVIDOR Y ACEPTAMOS LAS CONEXIONES ENTRANTES, SOLO UN CLIENTE SIMULTANEAMENTE
def arrancar_servidor():
    server.listen()
    while True:
        conn, direccion = server.accept()
        manejar_cliente(conn, direccion)




#LOGICA DEL SERVIDOR
def manejar_cliente(conn, direccion):
    print("Nueva conexion con: " + str(direccion))
    algoritmo = conn.recv(LONGITUD).decode(FORMATO)
    print(algoritmo)
    if algoritmo not in hashlib.algorithms_guaranteed:
        conn.sendall(b"EL ALGORITMO ESCOGIDO NO ES CORRECTO, ABORTANDO CONEXION")
        conn.close()
        return
    conn.sendall(b"ALGORITMO ADECUADO, PROCEDIENDO A VALIDAR LA TRANSACCION")
    mensaje, macMensaje = conn.recv(LONGITUD).decode(FORMATO).rsplit(' ', 1)
    
    macMensajeCalculado = hmac.new(key = CLAVE_CLIENTE.encode(FORMATO), msg = mensaje.encode(FORMATO), digestmod = algoritmo)

    if macMensajeCalculado.hexdigest() == macMensaje:
        print("OPERACION CORRECTA")
        conn.sendall(b"LA OPERACION SE HA REALIZADO CORRECTAMENTE")
    else:
        print(b"LA OPERACION NO SE HA PODIDO REALIZAR YA QUE EL MENSAJE HA SIDO MODIFICADO")
    #TODO COMPROBAR SI EL NONCE YA HA SIDO USADO ANTES
    conn.close()

arrancar_servidor()