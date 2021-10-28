#FUNCION QUE ESCRIBE ENE EL ARCHIVO LOGS CUANDO SE REALIZA UNA TRANSACCION 

def creaLog(transaccion, validez):
    f = open("logs.txt", "a")
    listaTransaccion =  transaccion.split() # [Cuenta origen, Cuenta destino, Cantidad, Mac]
    if validez:
        f.write("La transaccion : " + listaTransaccion[0] + " " +  listaTransaccion[1] + " " +  listaTransaccion[2] +
                " se realizo correctamente \n")
    else:
        f.write("Hubo un error con la transaccion : " + listaTransaccion[0] + " " +  listaTransaccion[1] + " " +
                 listaTransaccion[2] +" \n")
    f.close()


