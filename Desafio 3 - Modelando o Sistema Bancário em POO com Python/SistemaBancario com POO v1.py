"""/// TODO Recriar o sistema bancario dos desafios anteriores respeitando
hierarquia das classes.
    - Não é necessario fazer o codigo rodar.
    - Importante é montar as classes
    - Fazer uso do polimorfismo
    - Utilizar classes abstratas
    """

from abc import ABC, abstractmethod
from datetime import datetime
import textwrap


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

    def __str__(self):
        return f"Endereço: {self.endereco}\nNúmero de Contas: {len(self.contas)}"


class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

    def __str__(self):
        return f"Nome: {self.nome}, CPF: {self.cpf}, Data de Nascimento:{self.data_nascimento}, Endereço: {self.endereco}"


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @saldo.setter
    def saldo(self, valor):
        self._saldo = valor

    @property
    def numero(self):
        return self._numero

    @numero.setter
    def numero(self, valor):
        self._numero = valor

    @property
    def agencia(self):
        return self._agencia

    @agencia.setter
    def agencia(self, valor):
        self._agencia = valor

    @property
    def cliente(self):
        return self._cliente

    @cliente.setter
    def cliente(self, valor):
        self._cliente = valor

    @property
    def historico(self):
        return self._historico

    @historico.setter
    def historico(self, valor):
        self._historico = valor

    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\n@@@ Operação falhou, voce não tem saldo suficiente! @@@")

        elif saldo > 0:
            self.saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            return True

        else:
            print("\n@@@ Operação falhou! Valor inválido! @@@")

        return False

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            print("\n=== Deósito realizado com sucesso! ===")
            return True

        else:
            print("\n@@@ Operação falhou! Valor inválido! @@@")

            return False


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.
             transacoes if transacao["tipo"] == Saque.
             __name__]
        )

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("\n@@@ Operação falhou, valor de saque excede o limite! @@@")

        elif excedeu_saques:
            print("\n@@@ Operação falhou, limite de saques excedidos! @@@")

        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""\
        Agência:\t{self.agencia}
        C/C:\t\t{self.numero}
        Titular:\t{self.cliente.nome}
        """

    def mostrar_extrato(self):
        print("\n" + "=" * 11 + "  EXTRATO  " + "=" * 11)
        for transacao in self.extrato:
            print("\n" + transacao)
        print("\nSaldo atual: R${:.2f}\n".format(self.saldo))
        print("\n" + "=" * 33)


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self.transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime
                ("%d-%m-%Y %H:%M:%S"),
            }
        )


class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @classmethod
    @abstractmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def valor(self):
        return self.valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def valor(self):
        return self.valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


def depositar(clientes):
    cpf = cadastrar_cpf()
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado. Tente novamente. @@@")
        return

    conta = escolher_conta(cliente)
    if not conta:
        print("@@@ Operação cancelada ou conta não encontrada. @@@")
        return

    valor = float(input("\nInforme o valor do depósito: "))
    transacao = Deposito(valor)

    cliente.realizar_transacao(conta, transacao)


def sacar(clientes):

    cpf = cadastrar_cpf()
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado. Tente novamente. @@@")
        return

    conta = escolher_conta(cliente)
    if not conta:
        print("@@@ Operação cancelada ou conta não encontrada. @@@")
        return

    valor = float(input("\nInforme o valor do saque: "))
    transacao = Saque(valor)

    cliente.realizar_transacao(conta, transacao)


def mostrar_extrato(clientes):
    cpf = cadastrar_cpf()
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado. Tente novamente. @@@")
        return

    conta = escolher_conta(cliente)
    if not conta:
        print("@@@ Operação cancelada ou conta não encontrada. @@@")
        return

    print("\n=========== EXTRATO ===========")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "\n@@@ Não foram realizadas transações. @@@"
    else:
        for transacao in transacoes:
            print(f"{transacao['tipo']:>10}: R$ {transacao['valor']:.2f} - Data: {transacao['data']}")

    print(extrato)
    print(f"\n{'Saldo Atual:':>12} R$ {conta.saldo:.2f}")
    print("===========================")


def cadastrar_data():
    while True:
        data = input("\nDigite sua data de nascimento no formato dd/mm/aaaa:")
        try:
            data = datetime.strptime(data, "%d/%m/%Y")
            return data.strftime("%d/%m/%Y")
        except ValueError:
            print("\n@@@ Data inválida. Digite corretamente @@@")


def cadastrar_cpf():
    while True:
        cpf = input("\nDigite o seu CPF com 11 digitos (qualquer formato):")
        cpf = cpf.replace('.', '').replace('-', '').replace(' ', '')
        if len(cpf) == 11:
            return cpf
        else:
            print("\n@@@ O CPF informado é inválido. Tente novamente. @@@")


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
        cliente for cliente in clientes if cliente.cpf == cpf]
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

    cliente = PessoaFisica(nome=nome, data_nascimento=data,
                           cpf=cpf, endereco=endereco)

    clientes.append(cliente)

    print("\n=== Cliente cadastrado com sucesso! ===")


def criar_conta(numero_conta, clientes, contas):
    cpf = cadastrar_cpf()
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        ("\n@@@ Cliente nao encontrado, operação encerrada! @@@")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)
    print("\n===C/C número {} criada com sucesso!===".format(numero_conta))


def listar_contas(contas):
    for conta in contas:
        print(40 * "=")
        print(textwrap.dedent(str(conta)))


def listar_clientes(clientes):
    for cliente in clientes:
        print(40 * "=")
        print(textwrap.dedent(str(cliente)))


def escolher_conta(cliente):
    print("\nEscolha uma conta:")
    for i, conta in enumerate(cliente.contas, start=1):
        print(f"{i}. Conta Número: {conta.numero} - Saldo: R${conta.saldo:.2f}")
    escolha = int(input("\nNúmero da conta: ")) - 1
    if escolha >= 0 and escolha < len(cliente.contas):
        return cliente.contas[escolha]
    else:
        print("\n@@@ Escolha inválida. @@@")
        return None


def menu():
    print("""

============= MENU ================
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

    clientes = []
    contas = []

    while True:

        menu()

        escolha = input("\nEscolha uma opção: ")

        if escolha == '1':
            depositar(clientes)

        elif escolha == '2':
            sacar(clientes)

        elif escolha == '3':
            mostrar_extrato(clientes)

        elif escolha == '4':
            novo_cliente(clientes)

        elif escolha == '5':
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif escolha == '6':
            listar_contas(contas)

        elif escolha == '7':
            listar_clientes(clientes)

        elif escolha == '8':
            print("\nObrigado e até logo!")
            break

        else:
            print("\n@@@ Opção inválida. Por favor, tente novamente. @@@")


if __name__ == "__main__":
    main()
