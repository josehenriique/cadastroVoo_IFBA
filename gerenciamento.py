from datetime import date

class Gerenciamento:
    def __init__(self, name):
        self.name = name
    
    def cadastroVoo(self, numero, data, origem, destino):
    
        voo = {
            "numeroVoo" : numero,
            "dataVoo" : date(1090, 4, 2).isoformat(),
            "origemVoo" : origem,
            "destinoVoo" : destino,
            "vagasVoo" : 100,
        }

        return voo

    # def getVoos(self)