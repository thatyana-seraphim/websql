from sqlmodel import create_engine, SQLModel, Session
# Importamos os modelos para que o SQLModel saiba quais tabelas criar
from app.database.models import Curso, Professor, Aluno, Disciplina, DisciplinaCurso, Aula

# O arquivo será salvo na raiz do projeto (onde você roda o run.py)
sqlite_file_name = "database.sqlite"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# check_same_thread=False é necessário apenas para SQLite no FastAPI
engine = create_engine(sqlite_url, echo=False, connect_args={"check_same_thread": False})

def create_db_and_tables():
    """Cria o arquivo database.sqlite e as tabelas, se não existirem."""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Gerador de sessão para ser usado nas requisições da API."""
    with Session(engine) as session:
        yield session