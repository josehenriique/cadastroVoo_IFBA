from gerenciamento import Gerenciamento
from datetime import date

# Funções
def cadastroPerguntas(companhia):
    # Dados do voo
    numeroVoo = int(input("Digite o número do voo: "))
    diaMesAno = input("Digite a data do voo [DD/MM/AAAA]:")
    origem = int(input("Escolha do ponto de origem: "))
    destino = int(input("Escolha do ponto de destino: "))

    # Tratamendo da data
    data = diaMesAno.split("/")
    data.sort(reverse=True)

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

# Terminar cadastroDeAeroport()
def cadastroDeAeroporto(companhia):
    # Dados do aeroporto
    cidade = input("Digite a cidade do aeroporto: ")
    estado = input("Digite o estado do aeroporto: ")

    aeroporto = "{cidade}-{estado}"

    return aeroporto

# Código
companhiaUm = Gerenciamento("Azul")
cadastroPerguntas(companhiaUm)