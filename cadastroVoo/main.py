from gerenciamento import Gerenciamento
from datetime import date

# Funções
def cadastroVoo(companhia):
    # Dados do voo

    destinos = companhia.getDestinos()

    if destinos == []:
        print("Não há destinos cadastrados, por favor, adicione destinos primeiro!")
        return

    diaMesAno = input("Digite a data do voo [DD/MM/AAAA]:")

    print("")
    print("Escolha o ID do destino de origem e de chegada")
    showDestinos(companhia)
    print("")

    origem = int(input("Escolha do ponto de origem: "))
    destino = int(input("Escolha do ponto de destino: "))

    # Tratamendo da data
    data = diaMesAno.split("/")

    dados = {
        "dataVoo": data,
        "origem": destinos[origem - 1],
        "destino": destinos[destino - 1],
    }

    response = companhia.cadastroVoo(dados)

    if response['verification']:
        print("")
        print("Voo cadastrado com sucesso!")
    else:
        print("Falha no cadastro!")

def cadastroDeAeroporto(companhia):
    # Dados do aeroporto
    cidade = input("Digite a cidade (sem acentos): ")
    estado = input(f"Digite o estado de {cidade} (sem acentos): ")

    dados = {
        "cidade": cidade,
        "estado": estado
    }

    response = companhia.cadastroAeroporto(dados)

    if response["verification"]:
        print("")
        print("Aeroporto Cadastrado!")

def reservaAssento(companhia):

    voos = companhia.getVoos()

    for voo in voos:
        print("ID do Voo: ", voo["numeroVoo"])
        print("Data: ", voo["dataVoo"])
        print("{},{} -> {},{}".format(voo["origemVoo"]["cidade"], voo["origemVoo"]["estado"], voo["destinoVoo"]["cidade"], voo["destinoVoo"]["estado"]))
        print("")

    numVoo = int(input("Qual o número do voo (ID): "))
    vagasOcupadas = voos[numVoo - 1]["vagasOcupadas"]

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
        assentoEscolhido = int(input("Escolha um assento que não esteja ocupado [1-100]: "))

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

# Código

run = True
infoCompanhia = input("Informe a companhia para o painel de controle: ")

while run == True:
    companhia = Gerenciamento(infoCompanhia)

    print("--------------------------------------------------------------------")
    print("Sejam Bem-Vindo(a)! Essa é a lista de funções que você pode executar")
    print("")
    print("[1] Cadastrar voo")
    print("[2] Cadastrar aeroporto")
    print("[3] Mostrar Destinos")
    print("[4] Reserva de assentos")
    print("[5] Voos do Dia")
    print("[6] Sair")
    print("")
    funcao = int(input("Selecione a função que deseja executar: "))
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
            voosDoDia(companhia)
        case 6:
            run = False