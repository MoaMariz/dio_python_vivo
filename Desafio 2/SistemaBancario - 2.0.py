"""/// TODO Modificar o sistema da V1, adicionando funções para:
- Criação de Contas Individuais (Vinculadas, mas nao necessariamente unicas).
        - agencia (0001), numero da conta (inicia em 1), usuario vinculado
- Criação de Usuarios indiviuais (CPF unico).
        - nome, nascimento, cpf(somente numeros - string) e endereço.
            - endereço: logradouro, numero - bairro - cidade/ sigla estado.
* retorno das funções e suas chamdas são livres.
* passagem de argumentos sao obrigatorias da forma passada nas instruções
    - def saque (kwargs only - saldo, valor, extrato, limite, numero_saques,
      limite_saques)
    - def deposito (args only - saldo, valor, extrato).
    - def extrato (misto - arg saldo , kwarg extrato).
 - Criar funções para listar usuarios unicos e contas unicas."""


import time
from datetime import datetime
import textwrap

VALOR_MAXIMO = 500
LIMITE_SAQUES = 3
AGENCIA = "0001"


def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato.append("Depósito:\tR${:.2f}".format(valor))
        print("\n========== DEPOSITO =========")
        print("\nDepósito realizado no valor de : R${:.2f}".format(valor))
        print(("\n============================"))
    else:
        print("\n@@@ Operação falhou! O valor informado não é valido. @@@")
    return saldo, extrato


def sacar(*, saldo, valor, extrato,
          valor_maximo, numero_saques, limite_saques):

    if numero_saques >= limite_saques:
        print("\n" + "Limite de saques diários atingido.")
        print("\n" + "=" * 33)
        return saldo, extrato, numero_saques
    if valor > valor_maximo:
        print("\n@@@ O valor máximo para saque é de R${:.2f}. @@@".format(
            VALOR_MAXIMO))
        return saldo, extrato, numero_saques
    if saldo >= valor:
        saldo -= valor
        extrato.append("Saque: \t\tR${:.2f}".format(valor))
        numero_saques += 1
        print("\n=========== SAQUE ==========")
        print("\nSaque realizado no valor de : R${:.2f}".format(valor))
        print("\n============================")
    else:
        print("\n@@@ Saldo insuficiente. @@@")
    return saldo, extrato, numero_saques


def mostrar_extrato(saldo, /, *, extrato):
    print("=========  EXTRATO  =========")
    for transacao in extrato:
        print("\n" + transacao)
    print("\nSaldo atual: \tR${:.2f}\n".format(saldo))
    print("============================")


def cadastrar_data():
    while True:
        data = input("Digite a sua data de nascimento no formato dd/mm/aaaa: ")
        try:
            data = datetime.strptime(data, "%d/%m/%Y")
            return data.strftime("%d/%m/%Y")
        except ValueError:
            print("@@@ Data inválida. Digite corretamente @@@")


def cadastrar_cpf():
    while True:
        cpf = input("Digite o seu CPF com 11 digitos (qualquer formato):")
        cpf = cpf.replace('.', '').replace('-', '').replace(' ', '')
        if len(cpf) == 11:
            return cpf
        else:
            print("@@@ O CPF informado é inválido. Tente novamente. @@@")


def cadastrar_endereco():
    logradouro = input("Digite o logradouro (sem número): ")
    numero = input("Digite o número: ")
    bairro = input("Digite o bairro: ")
    cidade = input("Digite a cidade: ")
    estado = input("Digite a sigla do seu estado (ex: SP): ")

    endereco = "{}, {} - {} - {}/{}".format(logradouro,
                                            numero, bairro, cidade, estado)
    return endereco


def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [
        cliente for cliente in clientes if cliente["cpf"] == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def novo_cliente(clientes):
    cpf = cadastrar_cpf()

    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\n@@@ Erro! Já existe um cliente com esse CPF @@@")
        return

    nome = input("Digite seu nome: ")

    data = cadastrar_data()
    endereco = cadastrar_endereco()

    clientes.append({"nome": nome,
                     "data": data,
                     "cpf": cpf,
                     "endereço": endereco})
    print("\n=== Cliente cadastrado com sucesso! ===")


def criar_conta(agencia, numero_conta, clientes):
    cpf = cadastrar_cpf()
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\n===C/C número {} criada com sucesso!===".format(numero_conta))
        return {"agencia": agencia,
                "numero_conta": numero_conta,
                "cliente": cliente,
                }
    else:
        print("\n@@@ Cliente nao encontrado, operação encerrada! @@@")


def nova_conta(contas, clientes):
    numero_conta = len(contas) + 1
    conta = criar_conta(AGENCIA, numero_conta, clientes)
    if conta:
        contas.append(conta)


def listar_contas(contas):
    for conta in contas:
        linha = f"""\
        Agência:\t{conta['agencia']}
        C/C:\t\t{conta['numero_conta']}
        Titular:\t{conta['cliente']['nome']}
"""
        print(40 * "=")
        print(textwrap.dedent(linha))


def listar_clientes(clientes):
    for cliente in clientes:
        linha = f"""\
        Nome:\t\t\t{cliente['nome']}
        CPF:\t\t\t{cliente['cpf']}
        Data de Nascimento:\t{cliente['data']}
        Endereço:\t\t{cliente['endereço']}
"""
        print(40 * "=")
        print(textwrap.dedent(linha))


def menu():
    print("""
                MENU
Digite a operação desejada:

(1) Depositar
(2) Sacar
(3) Ver Extrato
(4) Novo Usuario
(5) Nova Conta
(6) Listar Contas
(7) Listas Usuarios
(8) Sair

==================================
""")


def main():

    saldo = 0
    numero_saques = 0
    extrato = []
    clientes = []
    contas = []

    while True:
        time.sleep(1)
        menu()

        escolha = input("\nEscolha uma opção: ")

        if escolha == '1':
            valor = float(input("\nDigite o valor do depósito: "))
            saldo, extrato = depositar(saldo, valor, extrato)

        elif escolha == '2':
            valor = float(input("\nDigite o valor do saque: "))
            saldo, extrato, numero_saques = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                valor_maximo=VALOR_MAXIMO,
                limite_saques=LIMITE_SAQUES,
                numero_saques=numero_saques,
            )
        elif escolha == '3':
            mostrar_extrato(saldo, extrato=extrato)

        elif escolha == '4':
            novo_cliente(clientes)

        elif escolha == '5':
            nova_conta(contas, clientes)

        elif escolha == '6':
            listar_contas(contas)

        elif escolha == '7':
            listar_clientes(clientes)

        elif escolha == '8':
            print("\nObrigado e até logo!")
            break

        else:
            print("\nOpção inválida. Por favor, tente novamente.")


if __name__ == "__main__":
    main()
