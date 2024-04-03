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

# Para melhorar a visualização vou dar pequena pausa na chamada do menu.
import time

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
            print("\n" + "=" * 11 + "  DEPOSITO  " + "=" * 11)

            print(
                "\nDepósito realizado no valor de : R${:.2f}".format(valor))
            print("\n" + "=" * 33)
        else:
            print("\nOperação falhou! O valor informado não é valido.")
            print("\n" + "=" * 33)

# Função de Saque
    def sacar(self, valor):
        if self.saques_diarios >= LIMITE_SAQUES:
            print("\nLimite de saques diários atingido.")
            print("\n" + "=" * 33)
            return
        if valor > VALOR_MAXIMO:
            print("\nO valor máximo para saque é de R${:.2f}.".format(
                VALOR_MAXIMO))
            print("\n" + "=" * 33)
            return
        if self.saldo >= valor:
            self.saldo -= valor
            self.extrato.append("Saque: R${:.2f}".format(valor))
            self.saques_diarios += 1
            print("\n" + "=" * 12 + "  SAQUE  " + "=" * 12)
            print("\nSaque realizado no valor de : R${:.2f}".format(valor))
            print("\n" + "=" * 33)
        else:
            print("Saldo insuficiente.")
            print("\n" + "=" * 33)

# Função Extrato
    def mostrar_extrato(self):
        print("\n" + "=" * 11 + "  EXTRATO  " + "=" * 11)
        for transacao in self.extrato:
            print("\n" + transacao)
        print("\nSaldo atual: R${:.2f}\n".format(self.saldo))
        print("\n" + "=" * 33)

# Definindo o estilo do Menu


def menu():
    print("""

                MENU

Digite a operação desejada:

(d) Depositar
(s) Sacar
(e) Ver Extrato
(q) Sair

==================================
""")

# Chamando a função principal - main - no loop infinito


def main():
    conta = ContaBancaria()
    while True:
        time.sleep(1)
        menu()

        escolha = input("\nEscolha uma opção: ").lower()

        if escolha == 'd':
            valor = float(input("\nDigite o valor do depósito: "))
            conta.depositar(valor)
        elif escolha == 's':
            valor = float(input("\nDigite o valor do saque: "))
            conta.sacar(valor)
        elif escolha == 'e':
            conta.mostrar_extrato()
        elif escolha == 'q':
            print("\nObrigado e até logo!")
            break
        else:
            print("\nOpção inválida. Por favor, tente novamente.")


if __name__ == "__main__":
    main()
