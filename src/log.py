def creaLog(transaccion, validez):
    f = open("logs.txt", "a")
    if validez:
        f.write("la transaccion " + transaccion + " se realizo correctamente \n")
    else:
        f.write("Hubo un error en la transaccion " + transaccion + "\n")
    f.close()
