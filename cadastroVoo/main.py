from gerenciamento import Gerenciamento
from datetime import date
import os
import json
import re

# Funções
def cadastroVoo(companhia):
    # Dados do voo

    destinos = companhia.getDestinos()

    if destinos == []:
        print("Não há destinos cadastrados, por favor, adicione destinos primeiro!")
        return

    diaMesAno = input("Digite a data do voo [DD/MM/AAAA]:")

    # Tratamendo da data
    data = diaMesAno.split("/")

    for number in data:
        if not number.isnumeric():
            print("")
            print("Data incorreta")
            return
        
    if len(data[0]) != 2:
        print("Formatação errada da data")
        return

    if len(data[1]) != 2:
        print("Formatação errada da data")
        return

    if len(data[2]) != 4:
        print("Formatação errada da data")  
        return

    print("")
    print("Escolha o ID do destino de origem e de chegada")
    showDestinos(companhia)
    print("")

    origem = int(input("Escolha do ponto de origem: "))
    destino = int(input("Escolha do ponto de destino: "))

    dados = {}

    try: 
        dados = {
            "dataVoo": data,
            "origem": destinos[origem - 1],
            "destino": destinos[destino - 1],
        }
    except:
        print("")
        print("Destinos não existentes")

    response = companhia.cadastroVoo(dados)

    if response['verification']:
        print("")
        print("Voo cadastrado com sucesso!")
    else:
        print("")
        print("Valores inválido!")

def cadastroDeAeroporto(companhia):
    # Dados do aeroporto
    cidade = input("Digite a cidade (sem acentos ou 'ç'): ")
    estado = input(f"Digite o estado de {cidade} (sem acentos, ex.: BA, RJ, SP, TO...): ").upper()

    def acentos(string):
        padrao = re.compile(r'[^\x00-\x7F]')
        resultado = padrao.search(string)

        if resultado:
            return True
        else:
            return False
    
    if acentos(cidade):
        print("")
        print("Uso de caracteres inválidos no espaço 'cidade'.")
        return
    
    if acentos(estado):
        print("")
        print("Uso de caracteres inválidos no espaço 'estado'.")
        return


    dados = {
        "cidade": cidade,
        "estado": estado
    }

    response = companhia.cadastroAeroporto(dados)

    if response["verification"]:
        print("")
        print("Aeroporto Cadastrado!")
    else:
        print("")
        print("Falha no cadastro de novo aeroporto!")

def reservaAssento(companhia):

    voos = companhia.getVoos()

    if voos == []:
        print("Não há voos cadastrados, por favor, adicione voos primeiro!")
        return

    for voo in voos:
        print("ID do Voo: ", voo["numeroVoo"])
        print("Data: ", voo["dataVoo"])
        print("{},{} -> {},{}".format(voo["origemVoo"]["cidade"], voo["origemVoo"]["estado"], voo["destinoVoo"]["cidade"], voo["destinoVoo"]["estado"]))
        print("")

    numVoo = None

    try:
        numVoo = int(input("Qual o número do voo (ID): "))
    except:
        print("")
        print("Digite um valor inteiro")
        return
    
    vagasOcupadas = None

    try:
        vagasOcupadas = voos[numVoo - 1]["vagasOcupadas"]
    except:
        print("")
        print("Esse aeroporto não existe")
        return


    if len(vagasOcupadas) == 100:
        print("Voo lotado!")
        return

    print("")
    print("Assentos Ocupados: ", )

    if vagasOcupadas == []:
        print("Nenhum assento reservado ainda!")
    else:
        for item in sorted(vagasOcupadas):
            print(item)

    print("")    

    assentoEscolhido = 0
    escolha = False

    while escolha == False:
        try:
            assentoEscolhido = int(input("Escolha um assento que não esteja ocupado [1-100]: "))
        except:
            print("")
            print("Valor inválido")
            return

        # Validação da escolha do assento

        if assentoEscolhido <= 0 or assentoEscolhido > 100:
            print("Assento inexistente!")
            escolha = False
            
        else:
            if vagasOcupadas == []:
                escolha = True
            else:
                for item in vagasOcupadas:
                    
                    if item == assentoEscolhido:
                        print("Assento já escolhido!")
                        escolha = False
                        break
                        
                    else:
                        escolha = True

    dados = {
        "assentoEscolhido": assentoEscolhido,
        "numVoo": numVoo
    }
    
    companhia.cadastrarAssento(dados)

def showDestinos(companhia):
    destinos = companhia.getDestinos()

    for destino in destinos:
        indice = destino["id"]
        cidade = destino["cidade"]
        estado = destino["estado"]

        print("")
        print("ID: ", indice)
        print(f"{cidade}, {estado}" )

def voosDoDia(companhia):

    companhia.getVoosDoDia()

def voosCompanhia(companhia):
    voos = companhia.getVoos()

    for voo in voos:
        print("ID do Voo: ", voo["numeroVoo"])
        print("Data: ", voo["dataVoo"])
        print("{},{} -> {},{}".format(voo["origemVoo"]["cidade"], voo["origemVoo"]["estado"], voo["destinoVoo"]["cidade"], voo["destinoVoo"]["estado"]))
        print("")

def showCompanhias():
    dbFile = os.path.join("db", "db.json")

    try:
        companhias = None

        with open(dbFile, 'r') as file:
            companhias = json.load(file)

        print("")
        print("Companhias: ")
        for companhia in companhias["companhias"]:
            print(companhia["companhia"])
        print("")
    except:
        return

# Código

run = True

showCompanhias()

# Escolhendo a companhia
infoCompanhia = None
verification_infoCompanhia = False

while verification_infoCompanhia == False:
    
    if infoCompanhia == None or infoCompanhia.strip() == "":
        infoCompanhia = input("Informe a companhia para o painel de controle: ").upper()
    else:
        verification_infoCompanhia: True
        break
        
companhia = Gerenciamento(infoCompanhia)

while run == True:

    print("--------------------------------------------------------------------")
    print("Sejam Bem-Vindo(a)! Essa é a lista de funções que você pode executar")
    print("")
    print("[1] Cadastrar voo")
    print("[2] Cadastrar aeroporto")
    print("[3] Mostrar destinos")
    print("[4] Reserva de assentos")
    print("[5] Voos da companhia")
    print("[6] Voos do dia")
    print("[7] Sair")
    print("")

    funcao = None

    try:
        funcao = int(input("Selecione a função que deseja executar: "))
    except:
        print("")
        print("Digite um valor inteiro")
    print("--------------------------------------------------------------------")

    match funcao:
        case 1:
            cadastroVoo(companhia)
        case 2:
            cadastroDeAeroporto(companhia)
        case 3:
            showDestinos(companhia)
        case 4:
            reservaAssento(companhia)
        case 5:
            voosCompanhia(companhia)
        case 6:
            voosDoDia(companhia)
        case 7:
            run = False
        case _:
            print("Não existe esse indice")


# Tratados
# cadastroDeVoos()
# cadastroDeAeroportos()
# resevarAssentos()