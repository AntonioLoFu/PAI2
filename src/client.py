import socket

HOST = '127.0.0.1'
FORMATO = "utf-8"
CABECERA = 128
CERRAR_CONEXION = "close_connection"
PORT = 65432
FALLO_VERIFICACION = "123"






#PROTOCOLO DE ENVIO DE DATOS AL SERVIDOR, PRIMERO SE INDICA EL NUMERO DE BYTES Y LUEGO SE MANDA EL MENSAJE COMO TAL
def enviarMensaje(mensaje, cliente):
    bytesMensaje = mensaje.encode(FORMATO)
    datos_cabecera = str(len(bytesMensaje)).encode(FORMATO)
    datos_cabecera += b' ' * (CABECERA - len(datos_cabecera))
    cliente.send(datos_cabecera)
    cliente.send(bytesMensaje)



def __main__():
    ruta = None
    #TODO PRINTEAR OPCIONES DEL CLIENTE
    print("BIENVENIDO")
    print("opciones:")
    print("1: ")
    print("2: ")
    print("3: ")
    while True:
        comando = input("Seleccione la opcion deseada\n")
        try:
            comando = int(comando)
        except ValueError:
            print("Introduzca un valor correcto\n")

        if comando == 1:
            #TODO FUNCION QUE REALICE LA OPCION 1
            pass
        elif comando == 2:
            #TODO FUNCION QUE REALICE LA OPCION 2
            pass

        elif comando == 3:
            #TODO FUNCION QUE REALICE LA OPCION 3
            pass

        
        else:
            print("Introduzca una opcion correcta")



            
__main__()