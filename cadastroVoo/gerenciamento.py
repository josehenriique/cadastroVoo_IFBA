from datetime import date

class Gerenciamento:
    def __init__(self, name):
        self.name = name
    
    def cadastroVoo(self, info):
    
        voo = {
            "numeroVoo" : info['numeroVoo'],
            "dataVoo" : date(int(info['dataVoo'][0]), int(info['dataVoo'][1]), int(info['dataVoo'][2])).isoformat(),
            "origemVoo" : info['origem'],
            "destinoVoo" : info['destino'],
            "vagasVoo" : 100,
        }

        return {"voo": voo, "verification": True}