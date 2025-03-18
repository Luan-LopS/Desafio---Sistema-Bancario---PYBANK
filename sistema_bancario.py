from datetime import datetime
import requests
from abc import ABC, abstractmethod


class Cliente:
    def __init__(self, _endereco):
        self._endereco = _endereco
        self._contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self._contas.append(conta)

    @property
    def endereco(self):
        return self._endereco

    @property
    def contas(self):
        return self._contas


class PessoalFisica(Cliente):
    def __init__(self, _cpf, _nome, _data_nascimento, endereco):
        super().__init__(endereco)
        self._cpf = _cpf
        self._nome = _nome
        self._data_nascimento = _data_nascimento

    @property
    def nome(self):
        return self._nome

    @property
    def cpf(self):
        return self._cpf


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = '0001'
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print(f'Saldo insuficiente, limite disponível R$ {self.saldo:.2f}')
            input('Pressione qualquer tecla para continuar')

        elif valor > 0:
            self._saldo -= valor
            print(f'''Saque realizado com sucesso!!!! 
    Saldo disponível ----------------------------- R$ {self.saldo:.2f}''')
            input('Pressione qualquer tecla para continuar')
            return True

        else:
            print('Saque falhou! Tente novamente')
            input('Pressione qualquer tecla para continuar')

        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print('Depósito realizado com sucesso!')
            input('Pressione qualquer tecla para continuar')
        else:
            print('Depósito falhou, tente novamente!')
            input('Pressione qualquer tecla para continuar')
            return False
        return True


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saque=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saque = limite_saque

    def sacar(self, valor):
        numero_saque = len([transacao for transacao in self.historico.transacoes if transacao['tipo'] == 'Saque'])

        excedeu_limite = valor > self.limite
        excedeu_saque = numero_saque >= self.limite_saque

        if excedeu_limite:
            print('''Valor de saque maior que o permitido.
        Entre em contato com o suporte: 99 99999-99999''')
            input('Pressione qualquer tecla para continuar')

        elif excedeu_saque:
            print('''Limite de saque diário foi atingido.
        Entre em contato com o suporte: 99 99999-99999''')
            input('Pressione qualquer tecla para continuar')

        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f'''
                Agência: \t{self.agencia}
                C/C:\t\t{self.numero}
                Titular:\t{self.cliente.nome}
                '''


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append({
            'tipo': transacao.__class__.__name__,
            'valor': transacao.valor,
            'data': datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        })


class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


def consulta_cep(cep):
    cep = str(cep)
    numero = input('Informe o número de sua residência: ')
    if len(cep) != 8:
        print('CEP inválido')
        return

    via_cep = f'https://viacep.com.br/ws/{cep}/json/'
    response = requests.get(via_cep)

    if response.status_code == 200:
        dados = response.json()

        if 'erro' in dados:
            print('Não encontramos o CEP')
        else:
            return f'{dados["logradouro"]}, {numero} - {dados["bairro"]} - {dados["localidade"]}/{dados["uf"]}'
    else:
        print('Erro na busca do CEP')


def criar_usuario(usuarios):
    print('Cadastro de usuário')
    nome_completo = input('Digite seu nome completo: ').strip().upper()
    if ' ' not in nome_completo:
        print('Entre com nome e sobrenome')
        return criar_usuario(usuarios)

    print('Digite a sua data de nascimento: ')
    data_nascimento = input('Entre com dia/mes/ano: ').strip()

    try:
        data_formatada = datetime.strptime(data_nascimento, '%d/%m/%Y')
    except:
        print('Entre com a data no formato dia/mes/ano')
        return criar_usuario(usuarios)

    CPF = input('Entre com o CPF: ').strip()
    if CPF in usuarios:
        print('Já existe um usuário com esse CPF. Tente novamente com outro CPF.')
        return criar_usuario(usuarios)

    cep = int(input('Entre com o CEP: ').strip())
    endereco = consulta_cep(cep=cep)

    usuario = {
        'nome': nome_completo,
        'data_nascimento': data_formatada.strftime('%d/%m/%Y'),
        'cpf': CPF,
        'endereco': endereco
    }

    usuarios[CPF] = usuario
    print(f'Nome: {usuario["nome"]} com o CPF: {usuario["cpf"]} nascido em {usuario["data_nascimento"]} residente em {usuario["endereco"]}')
    input('Pressione qualquer tecla para continuar')
    return usuarios


def main():
    usuarios = {}
    while True:
        escolha = int(input('''
        -----------Bem-vindo ao PyBank----------
                        **MENU**
        
            Escolha a opção que deseja:

            1) Cadastro de Usuário
            2) Criação de Conta Corrente
            3) Depósito
            4) Saque
            5) Extrato
            0) Sair

        -- '''))

        if escolha == 1:
            usuarios = criar_usuario(usuarios)

        elif escolha == 2:
            cpf = input('Digite seu CPF: ')
            if cpf in usuarios:
                numero_conta = len(usuarios[cpf].get('contas', [])) + 1
                print(f'Conta criada com sucesso -- Agência 0001 - Conta {numero_conta}')
                conta = ContaCorrente.numero_conta(numero_conta, usuarios[cpf])
                usuarios[cpf].adicionar_conta(conta)
            else:
                print('CPF não encontrado')

        elif escolha == 3:
            valor = float(input('Entre com o valor a ser depositado R$: ').strip())

        elif escolha == 4:
            print('====================Saque===================')
            print(f'Saldo atual: R$ {saldo:.2f}')
            valor = float(input('Digite o valor de saque R$: ').strip())
            # Lógica do saque

        elif escolha == 5:
            # Exibir extrato
            pass

        elif escolha == 0:
            print('Obrigado por usar nosso sistema!!!')
            break
        else:
            print('Opção inválida! Tente novamente.')

main()
