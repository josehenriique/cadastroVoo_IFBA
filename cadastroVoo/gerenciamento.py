from datetime import date
import os
import json

class Gerenciamento:

    # Verificador de arquivos vazios
    def _emptyFile(self, path):
        with open(path, 'r') as file:
            content = file.read()
            
        if not content:
            return True
        
    def _migracaoCompanhia(self, path, dado):
        with open(path, "r") as file:
            content = json.load(file)
        
        hasCompanhia = False

        for item in content:
            if item['companhia'] == dado["companhia"]:
                hasCompanhia = True
            else:
                hasCompanhia = False
        
        if not hasCompanhia:
            content.append(dado)
        
        with open(path, "w") as file:
            json.dump(content, file)
        
    def _readDataBase(self, path):
        with open(path, 'r') as file:
            content = json.load(file)

        return content    

    def __init__(self, name):
        self.name = name
        # Caminho do Banco de Dados
        self.dbPath = os.path.join("db", "db.json")

        emptyFileResponse = self._emptyFile(self.dbPath)

        if emptyFileResponse:
            with open(self.dbPath, 'w') as file:
                 json.dump([], file)

                 
        dados = {
            "companhia": self.name,
            "voos": []
        }
        
        self._migracaoCompanhia(self.dbPath, dados)

        # Variável com o conteúdo do banco de dados
        self.db = self._readDataBase(self.dbPath)

    def cadastroVoo(self, info):
        
        voo = {
            "numeroVoo" : info['numeroVoo'],
            "dataVoo" : date(int(info['dataVoo'][2]), int(info['dataVoo'][1]), int(info['dataVoo'][0])).isoformat(),
            "origemVoo" : info['origem'],
            "destinoVoo" : info['destino'],
            "vagasVoo" : 100,
        }
        
        companhias = self.db

        for companhia in companhias:
            if companhia["companhia"] == self.name:
                voosUpdate = companhia
                voosUpdate["voos"].append(voo)          
                break

        # Reescreve os voos atualizados no arquivo 
        with open(self.dbPath, 'w') as file:
            json.dump(companhias, file)
            return {"voo": voo, "verification": True}
    
    # def cadastroAeroporto(self, info):