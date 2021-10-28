from diffieTools import *

'''
Clase que implementa un objeto del tipo diffie-hellman, 
el constructor requiere un par de claves públicas y una privada.
Los métodos calculan la clave parcial y global. 

RECORDATORIO:

    un objeto dh1 = DH(publica1, publica2, privada) llegará 
    a la misma final que uno dh2 = DH(publica2, publica1, privada2)

    dh1.calculafinal(dh2.parcial)
'''

class DH(object):
    
    def __init__(self, publica1, publica2, privada):
        self.publica1 = publica1
        self.publica2 = publica2
        self.privada = privada
        self.final = None

    def calculaParcial(self):
        parcial = self.publica1**self.privada
        parcial = parcial%self.publica2
        return parcial

    def calculaFinal(self, parcial):
        final = parcial**self.privada
        final = final%self.publica2
        self.final = final
        return final

    
