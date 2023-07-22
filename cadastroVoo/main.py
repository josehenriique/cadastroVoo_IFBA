from gerenciamento import Gerenciamento
from datetime import date

# Funções
def cadastroVoo(companhia):
    # Dados do voo
    numeroVoo = int(input("Digite o número do voo: "))
    diaMesAno = input("Digite a data do voo [DD/MM/AAAA]:")
    origem = int(input("Escolha do ponto de origem: "))
    destino = int(input("Escolha do ponto de destino: "))

    # Tratamendo da data
    data = diaMesAno.split("/")

    dados = {
        "numeroVoo": numeroVoo,
        "dataVoo": data,
        "origem": origem,
        "destino": destino,
    }

    response = companhia.cadastroVoo(dados)

    if response['verification']:
        print("Voo cadastrado com sucesso!")
        print(response['voo'])
    else:
        print("Falha no cadastro!")

def cadastroDeAeroporto(companhia):
    # Dados do aeroporto
    cidade = input("Digite a cidade do aeroporto: ")
    estado = input("Digite o estado do aeroporto: ")

    dados = {
        "cidade": cidade,
        "estado": estado
    }

# Código
companhiaUm = Gerenciamento("Verde")

print("")
print("Sejam Bem-Vindo(a)! Essa é a lista de funções que você pode executar")
print("")
print("[1] Cadastrar voo")
print("")
funcao = int(input("Selecione a função que deseja executar: "))

match funcao:
    case 1:
        cadastroVoo(companhiaUm)