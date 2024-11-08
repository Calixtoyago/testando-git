<<<<<<< HEAD
print('Ola Mundo')
=======
import os
import time
import json
import string
import pwinput

maiuscula = (string.ascii_uppercase)
minuscula = (string.ascii_lowercase)
digitos = (string.digits)
cripto_senha = []
usuarios = []
acervo = []

# salvar os dados dos usuarios e dos livros em arquivos json
# toda função que fizer alterações nos usuários e/ou acervo terá o salvar_dados() dentro dela
def salvar_dados():
    with open('usuarios.json', 'w', encoding='utf8') as usuarios_json:
        json.dump(usuarios, usuarios_json, ensure_ascii=False, indent=2)

    with open('acervo.json', 'w', encoding='utf8') as acervo_json:
        json.dump(acervo, acervo_json, ensure_ascii=False, indent=2)

# pegar os dados já cadastrados no json para usar durante o sistema
def carregar_dados():
    global usuarios, acervo
    try:
        with open('usuarios.json', 'r', encoding='utf8') as usuarios_json:
            usuarios = json.load(usuarios_json)

        with open('acervo.json', 'r', encoding='utf8') as acervo_json:
            acervo = json.load(acervo_json)
    except FileNotFoundError:
        usuarios = []
        acervo = []


# limpa o terminal
# com entrada == True tem uma leve confirmação 
def limpar_terminal(entrada=False):
    if entrada:
        enter = input('\nPressione enter: ')
    time.sleep(0.4)
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


# recebe como parametro uma tupla com os valores numericos em string 
# exemplo: ('0', '1', '2')
# vão ser esses valores que a variavel opcao tera que obedecer
def escolha(opcao_tupla):
    while True:
        opcao = input('Insira sua escolha: ').lower().strip()
        if opcao not in (opcao_tupla):
            print('Selecione uma opção válida!')
        else:
            return opcao
            

# criptografia simples para as senhas
def cifraCesar(senha):
    if len(cripto_senha) == 0:
        cripto_senha.clear()

    if len(senha) == 0:
        senha_criptografada = ''.join(cripto_senha)
        cripto_senha.clear()
        return senha_criptografada

    if senha[0] in digitos:
        posicao = digitos.index(senha[0])
        if (posicao + 3) >= len(digitos):
            posicao = (posicao + 3) - len(digitos)
            cripto_senha.append(digitos[posicao])
        else:
            cripto_senha.append(digitos[posicao + 3])

    elif senha[0] in maiuscula:
        posicao = maiuscula.index(senha[0])
        if (posicao + 3) >= len(maiuscula):
            posicao = (posicao + 3) - len(maiuscula)
            cripto_senha.append(maiuscula[posicao])
        else:
            cripto_senha.append(maiuscula[posicao + 3])

    elif senha[0] in minuscula:
        posicao = minuscula.index(senha[0])
        if (posicao + 3) >= len(minuscula):
            posicao = (posicao + 3) - len(minuscula)
            cripto_senha.append(minuscula[posicao])
        else:
            cripto_senha.append(minuscula[posicao + 3])

    return cifraCesar(senha[1:])


# função para cadastrar novos usuarios
def cadastro(nome, senha, email, celular):
    novo_usuario = {
        'nome': nome,
        'senha': cifraCesar(senha),
        'email': email,
        'celular': celular,
        'livros': [],
        'is_admin': len(usuarios) == 0 # o primeiro usuario a cadastrar sera o administrador
    }                                  # a partir disso so administradores poderao tornar outros usuarios administradores
    usuarios.append(novo_usuario.copy())
    print('Cadastro realizado. Efetue o login.')
    salvar_dados()


# sistema de login
def login(nome, senha):
    for usuario in usuarios:
        if usuario['nome'] == nome and usuario['senha'] == cifraCesar(senha):
            print('Login realizado, seja bem vino!')
            return usuario
    print('Usuario ou senha incorreta!')
    return False




# funcao de menu para o login e cadastro
def menu_login():
    limpar_terminal()
    print('''
[0] Cadastrar
[1] Login
[2] Testar cadastro
''')    
    opcao = escolha(('0', '1', '2'))

    if opcao == '0': # cadastro
        nome = input('Nome: ')
        senha = pwinput.pwinput('Senha: ') #esconde a senha com *
        email = input('Email: ')

        while True:
            try:
                celular = input('Celular com DDD: [apenas os numeros] ')
                if len(celular) != 11 :
                    raise IndexError
                if not celular.isdigit():
                    raise ValueError
                celular = celular[:2]+' '+celular[2:7]+'-'+celular[7:]
            except IndexError:
                print('Error - Celular deve conter 11 numeros')
            except ValueError:
                print('Error - Celular deve conter apenas numeros')
            else:
                break

        cadastro(nome, senha, email, celular)
        salvar_dados()

    elif opcao == '1': # login
        nome = input('Usuario: ')
        senha = pwinput.pwinput('Senha: ')
        return  login(nome, senha)
    
    elif opcao == '2': # teste, depois vou tirar isso
        cadastro('Yago', '12345', 'yago@gmail.com', '2198765432')
        cadastro('Davi', '09876', 'davi@gmail.com', '40028922')
        cadastro('Eduardo', '12345', 'eduardo@gmail.com', '12345678')
    limpar_terminal(True)


# funcao principal, onde todas as outras funcoes serao invocadas
def menu():
    carregar_dados()
    usuario_ativo = None

    while not usuario_ativo:
        usuario_ativo = menu_login()
    # fim do login

    limpar_terminal(False)
    print(f'{" MENU PRINCIPAL ":-^60}')
       
# programa principal (so a def menu(), tudo ta dentro dela)
menu()
>>>>>>> biblioteca-login-cadastro
