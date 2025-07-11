
from dataSQL import BancoDeDados as sql
from cripto import Cripto as cripto




def main():
    # TO DO: Implementar a lógica principal do programa
    # Criar um usuario, com senha email e username
    # criar hash da senha e armazenala no banco de dados
    # quando o usuario quiser enviar uma mensagem ou arquivo, gerar as chaves RSA
    # criptografar a mensagem ou arquivo com a chave privada
    # descriptografar a mensagem ou arquivo com a chave publica
    # As chaves devem ser armazenadas no banco de dados com seus respectivos emissores e receptores
    # o usuario NÃO PODE ver a chave privada nem a publica de outro usuário.
    # O usuario pode ver sua propria chave privada e publica
    # armazenar as mensagens criptografadas no banco de dados para rodar testes com as chaves privadas de outros usuarios
    #criar três usuários para testes
    pass

    


banco = sql()
cripto = cripto()

banco.criar_sqlite()  # Cria o banco de dados e as tabelas necessárias


username = input("Digite o nome de usuário: ")
email = input("Digite o email: ")
senha = input("Digite a senha: ")
hash_senha = cripto.hash_senha(senha)
banco.inserir_usuario(username, email, hash_senha)
