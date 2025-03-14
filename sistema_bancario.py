from datetime import datetime
import requests

def criar_usuario(usuarios):
    print('Cadastro de usuario')
    nome_completo = input('Digite seu nome completo: ').strip().upper()
    if  ' ' not in nome_completo:
        print('Entre com nome e sobrenome')
        criar_usuario()

    print('Digite a sua data de nascimento: ')
    data_nascimento = input('Entre com dia/mes/ano: ').strip()

    try:
        data_formatada =  datetime.strptime(data_nascimento, '%d/%m/%Y')
    except:
        print('Entre com a data  no formato dia/mes/ano')

    CPF = input('Entre com o CPF: ').strip()
    if CPF in usuarios:
        print('Já existe um usuário com esse CPF. Tente novamente com outro CPF.')
        return criar_usuario()

    cep = int(input('Entre com o cep: ').strip())
    endereco = consulta_cep(cep=cep)

    usuario = {
        'nome': nome_completo,
        'data_nascimento': data_formatada.strftime('%d/%m/%Y'),
        'cpf':CPF,
        'endereco': endereco
    }

    usuarios[CPF] = usuario

    print(f'Nome: {usuario['nome']} com o CPF: {usuario['cpf']} nascido em {usuario['data_nascimento']} resitende em {usuario['endereco']} ')
    input('Precione qualquer tecla para continuar')
    return usuarios

def consulta_cep(cep):
    cep = str(cep)
    numero = input('Informe o numero de sua residencia: ')
    if len(cep) != 8:
        print('Cep invalido')
        return
    
    via_cep = f'https://viacep.com.br/ws/{cep}/json/'
    response  = requests.get(via_cep)

    if response.status_code == 200:
        dados = response.json()

        if 'erro' in dados:
            print('Não encontramos o CEP')
        else:
            return f'{dados['logradouro']}, {numero} - {dados['bairro']} - {dados['localidade']}/{dados['uf']}'
    else:
        print('Erro na buaca do CEP')

def criar_conta_corrente(usuarios):
    cpf = input('Digite seu cpf: ')
    if cpf in usuarios:
        criar_conta = input('Deseja criar um conta: y/n').strip().upper()

        agencia = '0001'

        if criar_conta == 'Y':
            numero_da_conta = len(usuarios[cpf].get('contas',[]))+1 
            print(f'Conta criada com susseco -- Agencia {agencia} - Conta {numero_da_conta}')

            conta = {
                'agencia': agencia,
                'numero_da_conta': numero_da_conta
            }

            usuarios[cpf]={}

            input('Precione qualquer tecla para continuar')


            if 'contas' not in usuarios[cpf]:
                usuarios[cpf]['contas'] = []
            return usuarios[cpf]['contas'].append(conta)     
        else:
            print('Crie uma conta')
    else:
        print('CPF não existe na base de dados')
def deposito(saldo, valor, list_deposito,/):
    print('Valor Invalido tente novamente') if valor <= 0 else list_deposito.append(valor)
    saldo += valor
    print('Deposito realizado com sucesso!!')
    return list_deposito, saldo
    
#deposito recebe argumentos positional only
#saldo
#valor
#extrato

#retorno
#saldo
#extrato

def saque(*, saldo, valor, valor_saque, limite_saque, list_saque):
    cont = 0

    if valor > 0:
        if limite_saque > cont:
            if valor_saque >= valor:
                if saldo > valor:
                    saldo -= valor
                    list_saque.append(valor)
                    cont += 1
                    print(f'''Saque realizado com sucesso!!!! 
    Saldo disponivel ----------------------------- R$ {saldo:.2f}''')
                    input('Precione qualquer tecla para continuar')
            
                else:
                    print(f'Saldo insuficiente limite disponivel R$ {saldo:.2f}')
                    input('Precione qualquer tecla para continuar')

            else:
                print('''Valor de saque maior que  o  permitido
        Entre em contato com o suporte 
            99 99999-99999''')
                input('Precione qualquer tecla para continuar')

        else:
            print('''Limite de saque diario foi atingindo
        Entre em contato com o suporte 
            99 99999-99999''')
            input('Precione qualquer tecla para continuar')
      
    else:
        print('Primeiro realize o deposito !')
        input('Precione qualquer tecla para continuar')

    return list_saque, saldo

#recebe os argumentos keyword only
# saldo 
# valor
# extrat
#limite
#numero_saques

#retorno
#saldo
#extrato


def extrato(saldo,/, list_deposito, list_saque):

    if saldo > 0:
        print('========================Extrato======================')

        for deposito in list_deposito:
            print(f'Deposito -------------------- + R$ {deposito:.2f}')

        print('___________________________________________________\n')

        for saque in list_saque:
            print(f'Saque -----------------------  - R$ {saque:.2f}')

        print(f'Saldo disponivel                         R$ {saldo}')
        
        print('=====================================================\n')

        input('Precione qualquer tecla para continuar')
    else:
        print('========================Extrato======================')
        print('Primeiro realize o deposito !')
        input('Precione qualquer tecla para continuar')

#argumentos positional only e keyword only
#position saldo
#nomerados extrato

def main():
    list_deposito =[]
    saldo = 0
    LIMITE_DE_SAQUE_DIARIO = 4
    VALOR_MAXIMO_SAQUE = 500

    while True:
        escolha = int(input('''
        -----------Bem vindo ao PyBank----------
                        **MENU**
        
            Escolha a opção que deseja
                            
            1) cadastro de Usuario
                        
            2) Criação de Conta corrente
        
            3) Deposito
                            
            4) Saque
                            
            5) Extrato
                            
        ########################################                        

            0) Sair
                
        -- '''))

        if escolha == 1:
            usuarios =  criar_usuario(usuarios={})

        elif escolha == 2:
            criar_conta_corrente(usuarios)
        
        elif escolha == 3:
            valor = float(input('Entre com o valor a ser depositado R$: ').strip())
            list_deposito, saldo = deposito(saldo, valor, list_deposito)

        elif escolha == 4:
            print('====================Saque===================')
            print(f'Saldo atual:               R$ {saldo:.2f}')
            valor = float(input('Digite valor de saque R$: ').strip())
            list_saque, saldo = saque(saldo=saldo, valor=valor, limite_saque=LIMITE_DE_SAQUE_DIARIO, list_saque=[], valor_saque=VALOR_MAXIMO_SAQUE)
        
        elif escolha == 5:
            extrato(saldo,list_deposito=list_deposito,list_saque=list_saque)

        elif escolha == 0:
            print('Obrigado por ter usado o nosso sistema!!!')
            break 
        
        else:
            print('Entre com uma opção valida!!!')
            input('Precione qualquer tecla para continuar')

main()