from typing import Optional
from datetime import date
from sqlmodel import SQLModel, Field

class Curso(SQLModel, table=True):
    __tablename__ = "CURSO"
    
    id: int = Field(primary_key=True)
    nome: Optional[str] = Field(default=None, max_length=25)
    totalcreditos: Optional[int] = Field(default=None)


class Professor(SQLModel, table=True):
    __tablename__ = "PROFESSOR"
    
    id: int = Field(primary_key=True)
    nome: Optional[str] = Field(default=None, max_length=30)
    admissao: Optional[date] = Field(default=None)
    areapesquisa: Optional[str] = Field(default=None, max_length=30)


class Aluno(SQLModel, table=True):
    __tablename__ = "ALUNO"
    
    id: int = Field(primary_key=True)
    nome: Optional[str] = Field(default=None, max_length=30)
    endereco: Optional[str] = Field(default=None, max_length=30)
    cidade: Optional[str] = Field(default=None, max_length=30)
    telefone: Optional[str] = Field(default=None, max_length=15)
    id_curso: Optional[int] = Field(default=None, foreign_key="CURSO.id")
    foto: Optional[bytes] = Field(default=None)       # Equivalente ao BLOB
    comentario: Optional[bytes] = Field(default=None) # Equivalente ao BLOB


class Disciplina(SQLModel, table=True):
    __tablename__ = "DISCIPLINA"
    
    id: int = Field(primary_key=True)
    nome: Optional[str] = Field(default=None, max_length=25)
    quantcreditos: Optional[int] = Field(default=None)


class DisciplinaCurso(SQLModel, table=True):
    __tablename__ = "DISCIPLINACURSO"
    
    id_disp: int = Field(foreign_key="DISCIPLINA.id", primary_key=True)
    id_curso: int = Field(foreign_key="CURSO.id", primary_key=True)


class Aula(SQLModel, table=True):
    __tablename__ = "AULA"

    id_aluno: int = Field(foreign_key="ALUNO.id", primary_key=True)
    id_disp: int = Field(foreign_key="DISCIPLINA.id", primary_key=True)
    id_prof: int = Field(foreign_key="PROFESSOR.id", primary_key=True)
    semestre: str = Field(max_length=7, primary_key=True)
    nota: Optional[float] = Field(default=None)

class UsuarioTentativa(SQLModel, table=True):
    __tablename__ = "usuario_tentativa"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    email: str = Field(index=True)
    num_exercicio: int = Field(index=True)
    tentativas: int = Field(default=0)
    acertos: int = Field(default=0)