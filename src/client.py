import hmac, hashlib, socket, secrets
from diffieTools import *
from diffieHellman import * 

HOST = '127.0.0.1'
FORMATO = "utf-8"
LONGITUD = 1024
PORT = 10000

ALGORITMOS_POSIBLES = ['sha224', 'sha256', 'sha1', 'md5']

#FUNCION QUE RECOGE LOS INPUTS DEL CLIENTE Y LOS EMPAQUETA EN UN MENSAJE

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
        
    algoritmo = input("INTRODUZCA EL ALGORITMO A USAR: {}\n".format(ALGORITMOS_POSIBLES))
    while True:
        if algoritmo in ALGORITMOS_POSIBLES:
            break
        print("INTRODUZCA UN ALGORITMO CORRECTO:")
        algoritmo = input("INTRODUZCA EL ALGORITMO A USAR: {}\n".format(ALGORITMOS_POSIBLES))


        
    mensaje = " ".join([cuenta_origen, cuenta_destino, cantidad])
    return (mensaje, algoritmo)

def __main__():
        
    while True:

            datos = getDatosUsuario()
            mensaje = " ".join([datos[0], secrets.token_hex()])
            
            #GENERAMOS LA CLAVE PÚBLICA Y PRIVADA DEL CLIENTE
            clientPublicKey = generaPrimoAleatorio(1, 100)
            clientPrivateKey = generaPrimoAleatorio(1, 100)
            
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))

                #RECIBIMOS LA CLAVE PÚBLICA DEL SERVER
                serverPublicKey = s.recv(LONGITUD).decode(FORMATO)
                
                #ENVIAMOS LA CLAVE PÚBLICA DEL CLIENTE
                s.sendall(str(clientPublicKey).encode(FORMATO))

                
                #CREAMOS UN OBJETO DH CON LAS CLAVES GENERADAS Y RECIBIDAS
                diffie = DH(int(serverPublicKey), clientPublicKey, clientPrivateKey)
                
                #LE ENVIAMOS AL SERVIDOR LA CLAVE PARCIAL DEL CLIENTE 
                s.sendall(str(diffie.calculaParcial()).encode(FORMATO))

                #RECIBIMOS LA CLAVE PARCIAL DEL SERVER
                serverParcial = s.recv(LONGITUD).decode(FORMATO)

                #CALCULAMOS LA CLAVE FINAL CON LA CLAVE PARCIAL DEL SERVER
                claveFinal = str(diffie.calculaFinal(parcial = int(serverParcial))).encode(FORMATO)

                #GENERAMOS EL HASHMAC DEL MENSAJE USANDO COMO CLAVE LA CLAVE FINAL
                hmacMensaje = hmac.new(key = claveFinal, 
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

                operacion = s.recv(1024).decode(FORMATO)
                print(operacion)        
__main__()