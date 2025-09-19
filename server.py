from typing import Annotated, List
from fastapi import Depends, FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from domain import engine, Item, Pessoa

#injecao dependencia
def get_session():
    with Session(engine) as session:
        yield session
SessionDep = Annotated[Session, Depends(get_session)]

# Inicializando o FastAPI
app = FastAPI()

# Habilitando CORS (Cross-Origin Resource Sharing)
origins = [
   "http://127.0.0.1/",
   "http://localhost/",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Quais origens podem acessar a API
    #allow_origins=[origins],
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos os métodos HTTP
    allow_headers=["*"],  # Permitir todos os cabeçalhos
)

@app.get("/")
async def root():
    return {"message": "SQL API"}

#select p.nome, c.nome from Pessoa p, Cargo c where p.idCargo=c.idCargo and p.cidade='Itajubá'
#/select/?p.nome&c.nome/from/?Pessoa=p&Cargo=c/where/p.idCargo=c.idCargo/and/p.cidade=Itajuba

# math(p:Pessoa-->c:Cargo) where return p.nome, c.nome
#

#@app.get("/selec/{attributes}/from/{dictionaries}/where/{expressions}")
#async def select(attributes: List[str], dictionaries: List[str], expressions: List[str]):
#    return ""

@app.get("/from/{clazz}", response_model=List)
async def get_from(clazz: str):
    res = []
    with Session(engine) as session:
        l = session.exec(select(Item).where(Item.clazz==clazz).order_by(Item.oid)).all()
        actOid = ""
        clazz = eval(clazz)
        obj = clazz()
        for i in l :
            if i.oid != actOid :
                if actOid != "" :
                    res.append(obj)
                actOid=i.oid
                obj = clazz()
            setattr(obj, i.key, i.value)
    return res

@app.get("/from/{clazz}/returns/", response_model=List)
async def get_select(clazz: str, keys: List[str] = Query()):
    print(clazz)
    print(keys)
    return []

@app.get("/returns/", response_model=List)
async def get_returns(dict: List[str] = Query(), key: List[str] = Query()):
    print(dict)
    print(key)
    return []