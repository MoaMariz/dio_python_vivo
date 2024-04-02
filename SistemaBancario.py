"""/// TODO Criar sistema de operações bancárias com:
- Operação Deposito : Deve ser posivel depositar valores positivos na
        conta.
    - Depositos devem ser armazenados em uma variavel e exibidos quando
        chamar o extrato
- Operação de Saque : Deve ser possivel realizar no maximo 3 saques
        diarios no limite de 500 reais por saque.
    - Caso nao tenha saldo em conta, exibir mensagem informando o usuario.
    - Saques devem ser armazenados em uma variavel e exibidos quando
        chamar o extrato
- Operação de Extrato : Listar todos os Depositos e Saques, exibindo ao
    final o saldo da conta corrente. Usar formatação de moeda."""

# Declarando variaveis estáticas
VALOR_MAXIMO = 500
LIMITE_SAQUES = 3


# Criando a classe ContaBancaria e suas funcionalidades


class ContaBancaria:
    def __init__(self):
        self.saldo = 0
        self.extrato = []
        self.saques_diarios = 0

# Função de Deposito
    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            self.extrato.append("Depósito: R${:.2f}".format(valor))
            print(
                "Depósito realizado no valor de : R${:.2f}".format(valor))
            print("-" * 35)
        else:
            print("Operação falhou! O valor informado não é valido.")
            print("-" * 35)

# Função de Saque
    def sacar(self, valor):
        if self.saques_diarios >= LIMITE_SAQUES:
            print("Limite de saques diários atingido.")
            print("-" * 35)
            return
        if valor > VALOR_MAXIMO:
            print("O valor máximo para saque é de R${:.2f}.".format(
                VALOR_MAXIMO))
            print("-" * 35)
            return
        if self.saldo >= valor:
            self.saldo -= valor
            self.extrato.append("Saque: R${:.2f}".format(valor))
            self.saques_diarios += 1
            print("Saque realizado no valor de : R${:.2f}".format(valor))
            print("-" * 35)
        else:
            print("Saldo insuficiente.")
            print("-" * 35)

# Função Extrato
    def mostrar_extrato(self):
        print("Extrato de transações:")
        for transacao in self.extrato:
            print(transacao)
        print("Saldo atual: R${:.2f}\n".format(self.saldo))
        print("-" * 35)

# Definindo o estilo do Menu


def menu():
    print("""

Digite a operação desejada:

(d) Depositar
(s) Sacar
(e) Ver Extrato
(q) Sair

------------------------------
""")

# Chamando a função principal - main - no loop infinito


def main():
    conta = ContaBancaria()
    while True:
        menu()

        escolha = input("Escolha uma opção: ").lower()

        if escolha == 'd':
            valor = float(input("Digite o valor do depósito: "))
            print("-" * 35)
            conta.depositar(valor)
        elif escolha == 's':
            valor = float(input("Digite o valor do saque: "))
            print("-" * 35)
            conta.sacar(valor)
        elif escolha == 'e':
            conta.mostrar_extrato()
            print("-" * 35)
        elif escolha == 'q':
            print("Obrigado e até logo!")
            break
        else:
            print("Opção inválida. Por favor, tente novamente.")


if __name__ == "__main__":
    main()
