from diffieTools import *

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

    
