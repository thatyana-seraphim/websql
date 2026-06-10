import os
from sqlmodel import create_engine, SQLModel, Session
from sqlalchemy import text
os.makedirs("data", exist_ok=True)

sqlite_url = "sqlite:///data/database.sqlite"

# check_same_thread=False é necessário apenas para SQLite no FastAPI
engine = create_engine(sqlite_url, echo=False, connect_args={"check_same_thread": False})

def create_db_and_tables():
    """Cria o arquivo database.sqlite e as tabelas, se não existirem."""
    SQLModel.metadata.create_all(engine)

    with engine.begin() as conn:
        result = conn.execute(text("SELECT COUNT(*) FROM aluno"))
        count = result.scalar()

        if count == 0:
            print("Banco de dados vazio. Executando seed.sql...")
            try:
                with open("seed.sql", "r", encoding="utf-8") as f:
                    sql_script = f.read()

                raw_conn = engine.raw_connection()
                try:
                    raw_conn.cursor().executescript(sql_script)
                    raw_conn.commit()
                    print("Banco populado com sucesso!")
                finally:
                    raw_conn.close()

            except FileNotFoundError:
                print("Aviso: Arquivo 'seed.sql' não foi encontrado na raiz do projeto.")
            except Exception as e:
                print(f"Erro ao popular o banco de dados: {e}")

def get_session():
    """Gerador de sessão para ser usado nas requisições da API."""
    with Session(engine) as session:
        yield session