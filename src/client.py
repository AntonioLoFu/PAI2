import socket
import hmac, hashlib
import secrets

HOST = '127.0.0.1'
FORMATO = "utf-8"
LONGITUD = 1024
CERRAR_CONEXION = "close_connection"
PORT = 65432
FALLO_VERIFICACION = "123"
CLAVE_CLIENTE = "clave_a_definir"






def getDatosUsuario():
    print("BIENVENIDO A LA APLICACION DE TRANSFERENCIAS BANCARIAS")
    cuenta_origen = input("INTRODUZCA LA CUENTA ORIGEN\n")
    while True:
        if cuenta_origen.isdigit():
            break
        print("INTRODUZCA UNA CUENTA CORRECTA")
        cuenta_origen = input("INTRODUZCA LA CUENTA ORIGEN\n")

    cuenta_destino = input("INTRODUZCA LA CUENTA DESTINO\n")
    while True:
        if cuenta_destino.isdigit():
            break
        print("INTRODUZCA UNA CUENTA CORRECTA")
        cuenta_destino = input("INTRODUZCA LA CUENTA DESTINO\n")
        

    cantidad = input("INTRODUZCA LA CANTIDAD A TRANSFERIR\n")
    while True:
        if cantidad.isdigit():
            break
        print("INTRODUZCA UNA CANTIDAD CORRECTA")
        cantidad = input("INTRODUZCA LA CANTIDAD A TRANSFERIR\n")
        

    algoritmo = input("INTRODUZCA EL ALGORITMO A USAR: {}\n".format(hashlib.algorithms_guaranteed))
    while True:
        if algoritmo in hashlib.algorithms_guaranteed:
            break
        print("INTRODUZCA UN ALGORITMO CORRECTO:")
        algoritmo = input("INTRODUZCA EL ALGORITMO A USAR: {}\n".format(hashlib.algorithms_guaranteed))


        
    mensaje = " ".join([cuenta_origen, cuenta_destino, cantidad])
    return (mensaje, algoritmo)
def __main__():
        
    while True:
        datos = getDatosUsuario()
        mensaje = " ".join([datos[0], secrets.token_hex()])
        hmacMensaje = hmac.new(key = CLAVE_CLIENTE.encode(FORMATO), msg = mensaje.encode(FORMATO), digestmod = datos[1])
        mensaje = " ".join([mensaje, hmacMensaje.hexdigest()])
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            #ENVIAMOS EL ALGORITMO A USAR PARA CALCULAR EL MAC DEL MENSAJE
            s.sendall(datos[1].encode(FORMATO))
            #RECIBIMOS LA RESPUESTA DE VERIFICACION DEL ALGORITMO
            print(s.recv(1024).decode(FORMATO))
            #ENVIAMOS EL MENSAJE CON EL NONCE Y EL MAC
            s.sendall(mensaje.encode(FORMATO))

            respuestaServidor = s.recv(1024).decode(FORMATO)
            print(respuestaServidor)


    



            
__main__()