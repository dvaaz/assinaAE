import sqlite3 as sql3

class BancoDeDados:
  def __init__(self, nome_db: str = "bancoHash.db"):
        self.db_name = nome_db
        self.__conexao = None
        self.__cursor = None

  def __conectar(self):
      try:
        self.__conexao = sql3.connect(self.db_name)
        self.__cursor = self.__conexao.cursor()
        return True
      except Exception as e:
        raise ("Error during connection:", e)
        return False

  def __desconectar(self):
    try:
      if self.__conexao:
        self.__conexao.close()
    except Exception as e:
      raise ("Error during disconnect:", e)
    finally:
      self.__conexao = None
      self.__cursor = None

  def criar_sqlite(self):
    try:
      self.__conectar()
      # Tabela de usuários
      self.__cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          nomeusuario TEXT NOT NULL UNIQUE,
                          email TEXT PRIMARY KEY NOT NULL UNIQUE,
                          senha_hash TEXT)''')
      # Tabelas para chaves públicas e privadas
      self.__cursor.execute('''CREATE TABLE IF NOT EXISTS publicKey (
                          emissor INTEGER NOT NULL,
                          receptor INTEGER NOT NULL,
                          chave TEXT NOT NULL,
                          FOREIGN KEY (emissor) REFERENCES usuarios(id),
                          FOREIGN KEY (receptor) REFERENCES usuarios(id))''')
      self.__cursor.execute('''CREATE TABLE IF NOT EXISTS privateKey(
                          emissor INTEGER NOT NULL,
                          receptor INTEGER NOT NULL,
                          chave TEXT NOT NULL,
                          FOREIGN KEY (emissor) REFERENCES usuarios(id),
                          FOREIGN KEY (receptor) REFERENCES usuarios(id))''')
      # Tabela de mensagens (mas só quem tem a chave privada pode ler ;-) )
      self.__cursor.execute('''CREATE TABLE IF NOT EXISTS mensagens (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          emissor INTEGER NOT NULL,
                          FOREIGN KEY (emissor) REFERENCES usuarios(id),
                          )    ''')
      # Tabela de status 0 para desbloqueado , 1 para bloqueado e -1 para excluído         
      self.__cursor.execute('''CREATE TABLE IF NOT EXISTS status (
                          id INTEGER PRIMARY KEY REFERENCES usuarios(id),
                          status INTEGER NOT NULL, 
                          )''')
      self.__conexao.commit()
      self.__desconectar()
      return True
    except:
      return False


  def inserir_usuario(self, nomeusuario, email, hash):
    try:
      self.__conectar()
      self.__cursor.execute("INSERT INTO usuarios (nomeusuario, email, senha_hash) VALUES (?, ?, ?)",
                            (nomeusuario, email, hash))
      self.__conexao.commit()
      self.__desconectar()
    except Exception as e:
        raise ("Erro ao inserir novo usuário: %s"% e)
        return False
    
  def gravar_chave_publica_privada(self, emissor, receptor, chavePub, chavePriv):
    try:
      self.__conectar()
      self.__cursor.execute("INSERT INTO publicKey (emissor, receptor, chave) VALUES (?, ?, ?)",
                            (emissor, receptor, chavePub))
      self.__cursor.execute("INSERT INTO privateKey (emissor, receptor, chave) VALUES (?, ?, ?)",
                            (emissor, receptor, chavePriv))
      self.__conexao.commit()
      self.__desconectar()
    except Exception as e:
      raise ("Erro ao gravar chaves: %s"% e)
      return False
  
  def utilizar_chave_publica(self, emissor, receptor):
    try:
      self.__conectar()
      self.__cursor.execute("Select chave FROM publicKey WHERE emissor = ? AND receptor = ?", (emissor, receptor))
      chave = self.__cursor.fetchone()
      self.__desconectar()
      if chave is not None:
        return chave[0]
      else:
        raise ValueError("Chave pública não encontrada para o emissor e receptor especificados.")
    except Exception as e:
      raise ("Erro ao utilizar chave pública: %s"% e)
      return False
  
  def utilizar_chave_privada(self, emissor, receptor):
    try:
      self.__conectar()
      self.__cursor.execute("Select chave FROM privateKey WHERE emissor = ? AND receptor = ?", (emissor, receptor))
      chave = self.__cursor.fetchone()
      self.__desconectar()
      if chave is not None:
        return chave[0]
      else:
        raise ValueError("Chave privada não encontrada para o emissor e receptor especificados.")
    except Exception as e:
      raise ("Erro ao utilizar chave privada: %s"% e)
      return False

  def procurar_usuario(self, email):
    if not self.__conectar():
      raise ConnectionError("Erro na conexao ao banco de dados")
    try:
      email = email.strip()
      self.__cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email))
      user = self.__cursor.fetchone()
      if user is not None:
        return True
      else:
        return False
    except Exception as e:
      raise ("Erro durante a consulta: %s"% e)

    finally:
      self.__desconectar()

    if user is not None:
      return True
    else:
      return False
  # confirma senha e status do usuário
  def confirmar_senha(self, login, hash):
      try:
        self.__conectar()
        hash_armazenado = None
        id_armazenado = None
        validar_id = False
        if login.cotains("@"):
          self.__cursor.execute("SELECT id FROM usuarios WHERE email = ?", (login))
          id_armazenado = self.__cursor.fetchone()

        else:
          self.__cursor.execute("SELECT id FROM usuarios WHERE nomeusuario = ?", (login))
          id_armazenado = self.__cursor.fetchone()

        if id_armazenado is None:
          raise ValueError("Usuário não encontrado")
        
        #verifica se o usuário está bloqueado ou excluído
        self.__cursor.execute("SELECT status FROM status WHERE id = ?", (id_armazenado[0],))
        validar_id = self.__cursor.fetchone()

        self.__desconectar()
        if validar_id[0] is not None:
          if validar_id[0] == 0:
            raise ValueError("Usuário bloquado, procure o administrador")
          elif validar_id[0] == -1:
            raise ValueError("Usuário excluído")
        
        if hash_armazenado is not None:
          return True
        else:
          return False

      except:
        raise ConnectionError ("Erro de conexao")

