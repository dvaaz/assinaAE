from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

from hashlib import sha256

# Classe para criptografia de dados
class Cripto:
    # inicia a conexão com o banco de dados
    def __init__(self):
        self.sql = sql()
    # Gera um par de chaves RSA e armazena no banco de dados
    def gerar_chaves(self, emissor, receptor): #recebe o emissor e receptor das chaves
        private_key = rsa.generate_private_key(
            public_exponent=65537, # Exponente público padrão
            key_size=2048, # Tamanho da chave em bits (indicado de 2048 bits até 4096 bits para maior segurança)
        )
        # Gera a chave pública a partir da chave privada
        public_key = private_key.public_key()

        # Serializar as chaves
        private_pem = private_key.private_bytes( 
            encoding=serialization.Encoding.PEM, 
            format=serialization.PrivateFormat.TraditionalOpenSSL, 
            encryption_algorithm=serialization.NoEncryption() # Não criptografa a chave privada, mas pode ser alterado para usar uma senha
        )
        # Serializa a chave pública
        # A chave pública é serializada no formato PEM, que é um formato de texto leg
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        # Armazenar as chaves no banco de dados
        
        return private_pem.decode('utf-8'), public_pem.decode('utf-8')
    
    # criptografa uma mensagem usando a chave privada buscada no banco de dados
    def criptografar_mensagem(self, mensagem, chave_privada):
        private_key = serialization.load_pem_private_key(
            chave_privada.encode('utf-8'),
            password=None,  # recomenda-se usar uma senha para protecao adicional
        )
        # Criptografa a mensagem usando a chave privada
        ciphertext = private_key.encrypt(
            mensagem.encode('utf-8'),
            padding.OAEP(  # Usa o padding OAEP para segurança adicional
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return ciphertext
    
    def descriptografar_mensagem(self, mensagem_criptografada, chave_publica):
        public_key = serialization.load_pem_public_key(
            chave_publica.encode('utf-8')
        )
        # Descriptografa a mensagem usando a chave pública
        plaintext = public_key.decrypt(
                 mensagem_criptografada,
                padding.OAEP(  
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return plaintext.decode('utf-8')
    
    # cria um Hash simples de senha
    def hash_senha(self, senha):

        # Cria um hash SHA-256 da senha
        senha_hash = sha256(senha.encode('utf-8')).hexdigest()
        return senha_hash