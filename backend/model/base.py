from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
import os
from sqlalchemy_utils import database_exists, create_database # Pode ser necessário importar aqui se não for usado em outro lugar

# Define o caminho do banco de dados (ajuste se db_path for diferente em outros lugares)
db_path = "database/"
# Verifica se o diretorio não existe
if not os.path.exists(db_path):
    # então cria o diretorio
    os.makedirs(db_path)

# url de acesso ao banco (essa é uma url de acesso ao sqlite local)
db_url = 'sqlite:///%s/alunos.sqlite3' % db_path

# cria a engine de conexão com o banco
engine = create_engine(db_url, echo=False)

# Cria a classe Base para o instanciamento de novos objetos.
Base = declarative_base()

# Instancia um criador de seção com o banco
Session = sessionmaker(bind=engine)

# cria o banco se ele não existir
if not database_exists(engine.url):
    create_database(engine.url)

# cria as tabelas do banco, caso não existam
Base.metadata.create_all(engine)