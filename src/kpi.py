def KPI():
    transacciones, transaccionesSatisfactorias = 0, 0

    with open("logs.txt", "r") as archivo:
        for line in archivo:
            transacciones += 1
            if ("correctamente" in line.strip()):
                transaccionesSatisfactorias += 1

    return transaccionesSatisfactorias/transacciones
