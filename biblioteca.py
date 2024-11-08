import os
import time
import json
import string
import pwinput

maiuscula = (string.ascii_uppercase)
minuscula = (string.ascii_lowercase)
digitos = (string.digits)
cripto_senha = []
generos_livros = (
    "Autoajuda", "Aventura", "Biografia",
    "Ciência", "Clássicos", "Ficção Científica",
    "Filosofia", "Fantasia", "História",
    "Humor", "Infantil", "Jovem Adulto",
    "Mistério", "Poesia", "Policial",
    "Religião", "Romance", "Suspense",
    "Tecnologia", "Terror"
)
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


# ver informações do perfil, incluindo os livros cadastrados nele
# a senha aparece escondida com o uso de #
def ver_perfil(usuario):
    print(f"{' Meu Perfil ':-^32}")
    for k, v in usuario.items():
        if k == 'senha':
            print(f"{k}: {'*'*len(v)}")
        elif k == 'livros':
            print('Livros: ')
            for livro in usuario[k]:
                print(f" - {livro['Titulo']} ({livro['Autor']})")
        else:
            print(f"{k}: {v}")


# mostra todos os livros no acervo
def mostrar_acervo():
    for id, livro in enumerate(acervo):
        print(f"{id}. {livro['Titulo']} ({livro['Autor']})")


# mostra as informacoes do livro selecionado pelo usuario anteriormente
def descricao_livro(titulo):
    for livro in acervo:
        if titulo == livro['Titulo']:
            print('\n','-'*20, sep='')
            for k,v in livro.items():
                print(f'{k}: {v}')
            print('-'*20,'\n')
            return
    
    print('Não há livro cadastrado com esse nome!')


# pega o livro selecionado pelo id da lista acervos e registra no perfil do usuario
def pegar_livro(usuario, id):
    if len(usuario['livros']) == 3:
        print('Você atingiu o limite de 3 livros emprestados ao mesmo tempo. \nCancele um livro para poder pegar outro')
        return

    try:
        id = int(id)
        usuario['livros'].append(acervo[id].copy())
        print(f'{acervo[id]['Titulo']} adicionado ao seu perfil')
        print('Muito obrigado! Tenha uma ótima leitura!')
        salvar_dados()
        return
    except ValueError:
        print('Insira um numero de id válido')
    except IndexError:
        print(f'Livro com id {id} nao encontrado')
        

# cancela o emprestimo de um livro no perfil do usuario
def cancelar_meus_livros(usuario):
    try:
        id = int(input('Id do livro a ser devolvido: [Numero a esquerda do titulo] '))
        usuario['livros'].pop(id)
        print('Livro removido do seu perfil!')
        salvar_dados()
        return
    except ValueError:
        print('Error - Id invalido')
    except IndexError:
        print(f'Error - Id nao encontrado')
        

# funcao que mostra os livros cadastrados no perfil do usuario
def ver_meus_livros(usuario):
    if len(usuario['livros']) == 0:
        print('Não há livros cadastrados em seu perfil')
        return False
    else:
        print(f'{'Meus Livros':-^21}')
        for i, livro in enumerate(usuario.get('livros')):
            print(f"[{i}] {livro['Titulo']}")


# remove um livro do sistema
def remover_livro():
    mostrar_acervo()
    try:
        id = input('Id do livro: [Numero a esquerda do titulo] ')
        id = int(id)
        livro_a_remover = acervo[id]     
        for usuario in usuarios:
            if livro_a_remover in usuario['livros']:
                usuario['livros'].remove(livro_a_remover)
        acervo.remove(livro_a_remover)
        salvar_dados()
    except ValueError:
        print('Insira um numero de id valido')
    except IndexError:
        print(f'Livro com id {id} nao encontrado')


# cadastra o livro e adiciona na lista acervo
def adicionar_livros(titulo, autor, paginas, isbn13, genero):
    livro = {
        'Titulo': titulo,
        'Autor': autor,
        'Paginas': paginas,
        'ISBN-13': isbn13,
        'Genero': genero,
    }
    acervo.append(livro.copy())
    salvar_dados()


# funcao com a entrada dos dados dos livros
def menu_cadastrar_livros():
    titulo = input('Titulo do livro: ')
    autor = input('Autor(a) do livro: ')

    while True:
        try:
            paginas = int(input('Quantidade de paginas: '))
        except ValueError:
            print('Error - Informe apenas numeros')
        else:
            break

    while True:
        try:
            isbn13 = input('Adicionar código ISBN-13: [apenas numeros] ')
            if isbn13.isdigit() == False or len(isbn13) != 13:
                raise ValueError 
            isbn13 = (isbn13[:3] + '-' +isbn13[3:])
        except ValueError:
            print('Error - Codigo ISBN invalido')
        else:
            break

    print('Generos Literátios: ')
    for i in range(len(generos_livros)):
        print(f'[{i}] {generos_livros[i]}')
    while True:
        try:
            id = int(input('Id do genero literario: [numero a esquerda do genero] '))
            genero = generos_livros[id]
        except ValueError:
            print('Error - Id invalido')
        except IndexError:
            print('Error - Genero selecionado nao encontrado')
        else:
            break

    adicionar_livros(titulo, autor, paginas, isbn13, genero)
    print('Livro adicionado!')
    limpar_terminal(True)


# funcao pra remover ou tornar um usuario administrador
def gerenciar_usuarios(id):
    try:
        user = usuarios[id]
        ver_perfil(user)
        print('''
    [0] Excluir usuário
    [1] Tornar administrador
            ''')
        opcao = escolha(('0', '1'))
        if opcao == '0':
            usuarios.pop(id)
            print('Usuário removido')
        elif opcao == '1':
            user['is_admin'] = True
            print(f"Usuário {user['nome']} agora é um administrador")
        salvar_dados()
    except TypeError:
        print('Error - Id invalido')
    except IndexError:
        print('Error - Usuario nao encontrado')


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


# funcao para a parte de pesquisar livros
def menu_pesquisar_livros(usuario_ativo):
    limpar_terminal()
    while True: 
        print(f'{' Pesquisar livro ':-^40}')
        if len(acervo) == 0:
            print('Não há livros cadastrados no momento')
            limpar_terminal(True)
            break

        else:
            mostrar_acervo()
            print('''
[0] Procurar livro
[1] Pegar um livro emprestado
[2] Voltar ao menu inicial'''
)
            while True:
                opcao = escolha(('0', '1', '2'))
                break
            if opcao == '0': # procurar livro, mostrando suas informacoes
                titulo = input('Titulo do livro: ')
                descricao_livro(titulo)
            elif opcao == '1': # cadastrar livro no perfil do usuario
                id = input('Numero do livro: [numero a esquerda do nome do livro] ')
                pegar_livro(usuario_ativo, id)
            elif opcao == '2': # voltar ao menu
                limpar_terminal(False)
                break
            limpar_terminal(True)


# funcao para o usuario ver os livros que possui em seu perfil
def menu_ver_meus_livros(usuario_ativo):
    limpar_terminal()
    ver_livros = ver_meus_livros(usuario_ativo)
    if ver_livros:
        print('''
[0] Ver informações de um livro
[1] Cancelar empréstimo de um livro
[2] Voltar ao menu principal
''')
        opcao = escolha(('0', '1', '2'))
        if opcao == '0': # ver informacoes de um livro
            titulo = input('Titulo do livro: ')
            descricao_livro(titulo)
            limpar_terminal(True)
        elif opcao == '1': # remover um livro do perfil, devolver o livro
            cancelar_meus_livros(usuario_ativo, id)
    limpar_terminal(True)


# funcao principal, onde todas as outras funcoes serao invocadas
def menu():
    carregar_dados()
    usuario_ativo = None

    while not usuario_ativo:
        usuario_ativo = menu_login()
    # fim do login

    while True:
        limpar_terminal(False)
        print(f'{" MENU PRINCIPAL ":-^60}')
        print(
'''[0] Sair
[1] Ver perfil
[2] Pesquisar livros
[3] Ver meus livros'''
)
        if usuario_ativo['is_admin'] == True:
            print(
'''[4] Adicionar livros no acervo
[5] Remover livros no acervo
[6] Editar informações dos livros
[7] Gerenciar usuários
[8] Testar cadastro de livros
'''
)
        if usuario_ativo['is_admin']:
            opcoes_disponiveis = ('0', '1', '2', '3', '4', '5', '6', '7', '8')
        else:
            opcoes_disponiveis = ('0', '1', '2', '3')
        opcao = escolha(opcoes_disponiveis)

        if opcao == '0': # sair da sua conta
            print('Volte sempre')
            limpar_terminal(True)
            menu()

        elif opcao == '1': # ver informacoes do perfil
            limpar_terminal()
            ver_perfil(usuario_ativo)
            limpar_terminal(True)

        elif opcao == '2': # pesquisar livros para adicionar ao seu perfil
            menu_pesquisar_livros(usuario_ativo)

        elif opcao == '3': # ver os livros cadastrados no seu perfil
            menu_ver_meus_livros(usuario_ativo)
            
        # opcoes exclusivas do administrador
        if usuario_ativo['is_admin']:
            if opcao == '4': # adicionar livros no acervo
                menu_cadastrar_livros()

            elif opcao == '5': # remover livros do acervo, e consequentemente dos usuarios
                remover_livro()
                print('Livro removido!')
                limpar_terminal(True)

            elif opcao == '6': # editar livros, preguica de fazer isso
                print('editando livros')

            elif opcao == '7': # gerenciar usuarios
                for posicao, usuario in enumerate(usuarios):
                    print(f"{posicao}. {usuario.get('nome')}")
                id = input('\nId do usuario: [numero a esquerda do usuario] ')
                gerenciar_usuarios(id)
                limpar_terminal(True)

            elif opcao == '8': # teste do cadastro de livros
                adicionar_livros('Harry Potter', 'J.K. Rowling', '264', '978-8532511010', 'Fantasia')
                adicionar_livros('Duna', 'Frank Helbert', '680', '978-8576573135', 'Ficção Científica' )
                adicionar_livros('Morro dos Ventos Uivantes', 'Emily Bronte', '368', '978-8594318237', 'Clássicos')
        
# programa principal (so a def menu(), tudo ta dentro dela)
menu()
