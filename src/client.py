import socket
import hmac, hashlib
import secrets
from diffieTools import *
from diffieHellman import * 

HOST = '127.0.0.1'
FORMATO = "utf-8"
LONGITUD = 1024
CERRAR_CONEXION = "close_connection"
PORT = 10000
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
            

            #GENERAMOS LA CLAVVE PÚBLICA Y PRIVADA DEL CLIENTE
            clientPublicKey = generaPrimoAleatorio(1, 100)
            clientPrivateKey = generaPrimoAleatorio(1, 100)
            print("Clave privada del cliente" + str(clientPrivateKey))
            print("Clave publica del cliente" + str(clientPublicKey))
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                #ENVIAMOS LA CLAVE PÚBLICA DEL CLIENTE
                s.sendall(str(clientPublicKey).encode(FORMATO))
                #RECIBIMOS LA CLAVE PÚBLICA DEL SERVER
                serverPublicKey = s.recv(LONGITUD).decode(FORMATO)
                
                diffie = DH(publica1 =  int(serverPublicKey), publica2 =clientPublicKey, privada = clientPrivateKey)
                
                print("Clave parcial del cliente" + str(diffie.calculaParcial()))
                s.sendall(str(diffie.calculaParcial()).encode(FORMATO))
                serverParcial = s.recv(LONGITUD).decode(FORMATO)
                print("Clave parcial del servidor recibida por el cliente" + serverParcial)
                claveFinalCliente = str(diffie.calculaFinal(parcial = int(serverParcial))).encode(FORMATO)
                print(claveFinalCliente)
                hmacMensaje = hmac.new(key = claveFinalCliente, 
                                msg = mensaje.encode(FORMATO), 
                                digestmod = datos[1])

                mensaje = " ".join([mensaje, hmacMensaje.hexdigest()])
                #ENVIAMOS EL ALGORITMO A USAR PARA CALCULAR EL MAC DEL MENSAJE
                s.sendall(datos[1].encode(FORMATO))
                #RECIBIMOS LA RESPUESTA DE VERIFICACION DEL ALGORITMO
                print(s.recv(1024).decode(FORMATO))
                #ENVIAMOS EL MENSAJE CON EL NONCE Y EL MAC
                s.sendall(mensaje.encode(FORMATO))

                respuestaServidor = s.recv(1024).decode(FORMATO)
                print(respuestaServidor)


    



            
__main__()