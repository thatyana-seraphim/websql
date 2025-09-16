import uuid
from sqlmodel import SQLModel, Session, select, create_engine, Field
from typing import Optional
# Definição do banco de dados SQLite
DATABASE_URL = "sqlite:///./data/websql.db"
engine = create_engine(DATABASE_URL, echo=True)
#Persistence
class Item(SQLModel, table=True):
    __tablename__="key"    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    oid : str = Field(index=True)
    dictionary : Optional[str] = None
    key : Optional[str] = None
    value : Optional[str] = None

class Pessoa(SQLModel, table=False) :
    oid : str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    nome: Optional[str] = None
    profissao: Optional[str] = None

if __name__=="__main__":    
    # Criação do banco de dados
    SQLModel.metadata.create_all(bind=engine) 

    with Session(engine) as se:
        p = Pessoa(nome="enzo", profissao="professor")
        for ch, val  in p.__dict__.items() :
            #print(ch, val)
            d = Item(oid=p.oid, dictionary=p.__class__.__name__, key=ch, value=val)
            se.add(d)
        se.commit()

        item = se.exec(select(Item)).all()
        for d in item :
            print(d.oid, d.key, d.value)

        # b6eb9419-6b1d-48ea-b0a3-c20ed324b176
        prim = se.exec(select(Item).where(Item.oid=="b6eb9419-6b1d-48ea-b0a3-c20ed324b176").order_by(Item.oid)).all()
        clazz = eval("Pessoa")
        novo=clazz()
        for d in prim :
            setattr(novo, d.key, d.value)
            print(d.dictionary, d.key, d.value)
        

        print(novo.oid, novo.nome, novo.profissao)

        res = []
        l = se.exec(select(Item).where(Item.dictionary=="Pessoa").order_by(Item.oid)).all()
        actOid = ""
        obj = clazz()
        for i in l :
            if i.oid != actOid :
                if actOid != "" :
                    res.append(obj)
                actOid=i.oid
                obj = clazz()
            setattr(obj, i.key, i.value)
        print(len(res))
        for i in res :
            print(i.__class__.__name__, i)
