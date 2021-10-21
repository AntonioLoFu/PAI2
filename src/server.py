import socket, json
HOST = "127.0.0.1"
PORT = 65432
CABECERA = 128
FORMATO = "utf-8"
CERRAR_CONEXION = "close_connection"
FALLO_VERIFICACION = "123"
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

#PROTOCOLO DE ENVIO DE DATOS AL SERVIDOR, PRIMERO SE INDICA EL NUMERO DE BYTES Y LUEGO SE MANDA EL MENSAJE COMO TAL
def enviarMensaje(mensaje, cliente):
    bytesMensaje = mensaje.encode(FORMATO)
    datos_cabecera = str(len(bytesMensaje)).encode(FORMATO)
    datos_cabecera += b' ' * (CABECERA - len(datos_cabecera))
    cliente.send(datos_cabecera)
    cliente.send(bytesMensaje)

#ARRANCAMOS EL SERVIDOR Y ACEPTAMOS LAS CONEXIONES ENTRANTES, SOLO UN CLIENTE SIMULTANEAMENTE
def arrancar_servidor():
    server.listen()
    while True:
        conn, direccion = server.accept()
        manejar_cliente(conn, direccion)




#LOGICA DEL SERVIDOR
def manejar_cliente(conn, direccion):
    print("Nueva conexion con: " + str(direccion))
    while True:
        print("ESPERANDO RECIBIR MENSAJE")
        mensaje_recibido = conn.recv(CABECERA) 
        if mensaje_recibido:
            print(mensaje_recibido.decode(FORMATO))
            datos = conn.recv(int(mensaje_recibido.decode(FORMATO))).decode(FORMATO)
            if datos == "1":
                #TODO MANEJAR FUNCION DEL CLIENTE
                pass
            elif datos == "2":
                #TODO MANEJAR FUNCION DEL CLIENTE
                pass
            elif datos == "3":
                #TODO MANEJAR FUNCION DEL CLIENTE
                pass
                
            elif datos == CERRAR_CONEXION:
                break
    
    conn.close()



arrancar_servidor()