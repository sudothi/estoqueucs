import os

ARQUIVO_ESTOQUE = 'estoque.txt'

# Carregamento do arquivo do estoque
def carregar_estoque():
    estoque = {}
    # Caso o arquivo exista, vamos carregar ele
    if os.path.exists(ARQUIVO_ESTOQUE): # Verifica se o aruqivo existe
        arquivo = open(ARQUIVO_ESTOQUE, 'r')
        for linha in arquivo: # Vamos de linha em linha pegando os produtos
            partes = linha.strip().split(',') # Agora temos um array com a informaçao da linha
            # Arrumando cada produto
            nome = partes[0]
            preco = float(partes[1])
            quantidade = int(partes[2])
            estoque[nome] = (preco, quantidade) # Agora criamos um produto ligado a um preço e uma quantidade
        arquivo.close()
    return estoque

# Salvar estoque no arquivo
def salvar_estoque(estoque):
    arquivo = open(ARQUIVO_ESTOQUE, 'w')
    for nome in estoque:
        preco, quantidade = estoque[nome]
        arquivo.write(nome + ',' + str(preco) + ',' + str(quantidade) + '\n')
    arquivo.close()

# Mostrar produtos do estoque
def mostrar_estoque(estoque):
    print("\nEstoque:")
    for nome in estoque:
        preco, quantidade = estoque[nome]
        print(nome, "- R$", preco, "- Quantidade:", quantidade)

# Pequena funçao para mostrar o carrinho
def mostrar_carrinho(carrinho):
    print("\nCarrinho:")
    total = 0
    for nome in carrinho:
        preco, quantidade = carrinho[nome]
        subtotal = preco * quantidade
        print(nome, "-", quantidade, "x R$", preco, "= R$", subtotal)
        total = total + subtotal
    print("Total: R$", total)

# Programa começa aqui
estoque = carregar_estoque()

# Se estoque estiver vazio, criamos alguns produtos default
if len(estoque) == 0:
    estoque['Defletor de Ar'] = (99.90, 10)
    estoque['Escapamento Esportivo'] = (2000.00, 5)
    estoque['Tanques de agua'] = (500.80, 8)
    estoque['Engate de reboque'] = (1000.49, 3)
    estoque['Iluminaçao de teto'] = (59.90, 20)
    estoque['Radio PX'] = (249.90, 1)
    estoque['Aquecedor de cabine'] = (159.90, 4)
    estoque['Placas decorativas'] = (30.00, 36)
    estoque['Pingentes de espelho'] = (14.90, 98)
    estoque['Monitor de ponto cego'] = (869.90, 2)
    salvar_estoque(estoque)

carrinho = {}

while True:
    mostrar_estoque(estoque)
    print("\nDigite o nome do produto para comprar")
    print("Ou digite 'finalizar' para comprar ou 'sair' para sair")
    escolha = input("Escolha: ")

    if escolha == 'sair':
        print("Saindo.")
        break

    if escolha == 'finalizar':
        mostrar_carrinho(carrinho)
        salvar_estoque(estoque)
        print("Compra finalizada!")
        carrinho = {}
        continue

    if escolha in estoque:
        qtd_txt = input("Quantidade para comprar: ")
        if qtd_txt.isdigit(): # Apenas para evitar bugs
            quantidade = int(qtd_txt)
            preco, qtd_disponivel = estoque[escolha]
            if quantidade > 0 and qtd_disponivel >= quantidade: # Vendo se temos produtos suficientes
                estoque[escolha] = (preco, qtd_disponivel - quantidade)
                if escolha in carrinho:
                    preco_c, qtd_c = carrinho[escolha]
                    carrinho[escolha] = (preco_c, qtd_c + quantidade)
                else:
                    carrinho[escolha] = (preco, quantidade)
                mostrar_carrinho(carrinho)
            else:
                print("Quantidade inválida ou insuficiente no estoque.")
        else:
            print("Digite apenas números.")
    else:
        print("Produto não encontrado.")

