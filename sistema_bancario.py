
#saque = 0
saldo = 0
LIMITE_DE_SAQUE_DIARIO = 3
VALOR_MAXIMO_SAQUE = 500
cont = 0
list_deposito = []
list_saque = []

def deposito(list_deposito):
    global saldo
    saldo += float(input('Entre com o valor a ser depositado R$: '))
    print('Valor Invalido tente novamente') if saldo <= 0 else list_deposito.append(saldo)
    return list_deposito
    

def valor_saque(list_saque):
    global cont
    global saldo
    print('====================Saque===================')
    print(f'Saldo atual:               R$ {saldo:.2f}')
    saque = float(input('Digite valor de saque R$: '))


    if saldo > 0:
        if LIMITE_DE_SAQUE_DIARIO > cont:
            if VALOR_MAXIMO_SAQUE >= saque:
                if saldo > saque:
                    saldo -= saque
                    list_saque.append(saque)
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

    return list_saque


def extrato(list_deposito, list_saque):
    global saldo

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


    

def menu():
    escolha = int(input('''
    -----------Bem vindo ao PyBank----------
    
          Escolha a opção que deseja
    
          1) Deposito
                        
          2) Saque
                        
          3) Extrato
                        
    ########################################                        

          0) Sair
            
    -- '''))

    if escolha == 1:
        deposito(list_deposito)
    elif escolha == 2:
        valor_saque(list_saque)
    elif escolha == 3:
        extrato(list_deposito, list_saque)
    elif escolha == 0:
        print('Obrigado por ter usado o nosso sistema!!!')
        return False 

    else:
        print('Entre com uma opção valida!!!')
        input('Precione qualquer tecla para continuar')

while True:
    if menu() == False:
        break
