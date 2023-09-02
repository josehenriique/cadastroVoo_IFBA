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

        for item in content["companhias"]:
            if item['companhia'] == dado["companhia"]:
                hasCompanhia = True
                break
            else:
                hasCompanhia = False
        
        if not hasCompanhia:
            content["companhias"].append(dado)
        
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

        if not os.path.exists(self.dbPath):
            with open(self.dbPath, 'w') as file:
                file.write("")

        emptyFileResponse = self._emptyFile(self.dbPath)

        if emptyFileResponse:
            with open(self.dbPath, 'w') as file:
                 json.dump({
                    "companhias": [],
                    "destinos": []
                 }, file)
    
        dados = {
            "companhia": self.name,
            "voos": []
        }
        
        self._migracaoCompanhia(self.dbPath, dados)

        # Variável com o conteúdo do banco de dados
        self.db = self._readDataBase(self.dbPath)

    def cadastroVoo(self, info):
                
        companhias = self.db

        # Atualização do número do voo de forma automática
        indice = 0

        for companhia in companhias["companhias"]:
            if companhia["companhia"] == self.name:
                quantidadeDeVoos = len(companhia["voos"])
                indice = quantidadeDeVoos

                break 
        
        voo = {}

        try:
            voo = {
                "numeroVoo" : indice + 1,
                "dataVoo" : date(int(info['dataVoo'][2]), int(info['dataVoo'][1]), int(info['dataVoo'][0])).isoformat(),
                "origemVoo" : info['origem'],
                "destinoVoo" : info['destino'],
                "vagasOcupadas" : [],
            }
        except:
            return {"voo": voo, "verification": False}

        # Atualização dos voos na estrutura de dados

        for companhia in companhias["companhias"]:
            if companhia["companhia"] == self.name: 

                voosUpdate = companhia
                voosUpdate["voos"].append(voo)
                break

        # Reescreve os voos atualizados no arquivo 
        with open(self.dbPath, 'w') as file:
            json.dump(companhias, file)
            return {"voo": voo, "verification": True}
    
    def cadastroAeroporto(self, info):
        destinos = self.db

        try:
            # Caso não tenha nenhuma destino
            if destinos["destinos"] == []:

                indice = 1
                dados = {
                    "id": indice,
                    "cidade": info["cidade"],
                    "estado": info["estado"]
                }

                destinos["destinos"].append(dados)

                with open(self.dbPath, 'w') as file:
                    json.dump(destinos, file)
                    return {"destino": dados, "verification": True}
            
            # Verificação para não haver destinos iguais
            hasDestino = False

            for item in destinos["destinos"]:
                if item["cidade"] == info["cidade"]:
                    hasDestino = True
                    break
                else:
                    hasDestino = False
            
            # Atualização de um novo destino
            if not hasDestino:

                newIndice = int(destinos["destinos"][-1]["id"]) + 1
            
                dados = {
                    "id": newIndice,
                    "cidade": info["cidade"],
                    "estado": info["estado"]
                }
                
                destinos["destinos"].append(dados)
                
                with open(self.dbPath, 'w') as file:
                    json.dump(destinos, file)
                    return {"destino": dados, "verification": True}
            
        except:
            return {"destino": dados, "verification": False}

    def getDestinos(self):
        destinos = self.db["destinos"]

        return destinos

    def getVoos(self):

        companhias = self.db

        for companhia in companhias["companhias"]:
            if companhia["companhia"] == self.name:
                voos = companhia["voos"]
                break

        return voos
    
    def cadastrarAssento(self, info):

        db = self.db

        numVoo = info["numVoo"]
        assentoEscolhido = info["assentoEscolhido"]

        for companhia in db["companhias"]:
            if companhia["companhia"] == self.name:
                
                vagasUpdate = companhia["voos"][numVoo - 1]
                vagasUpdate["vagasOcupadas"].append(assentoEscolhido)

                break
        
        
        with open(self.dbPath, "w") as file:
            json.dump(db, file)
            return {"verification": True}
        
    def getVoosDoDia(self):
        
        companhias = self.db
        dataAtual = str(date.today())

        print("Data atual: ", dataAtual)
        for companhia in companhias["companhias"]:
            print("")
            print(companhia["companhia"], ":")
            print("")

            for voo in companhia["voos"]:
                if voo["dataVoo"] == dataAtual:
                    print("ID do Voo: ", voo["numeroVoo"])
                    print("Data:", voo["dataVoo"])
                    print("Rota: {},{} -> {},{}".format(voo["origemVoo"]["cidade"], voo["origemVoo"]["estado"], voo["destinoVoo"]["cidade"], voo["destinoVoo"]["estado"]))
                    print("")
                    print("")