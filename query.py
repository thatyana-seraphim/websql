from sqlmodel import Session, select
from domain import Item, engine, Pessoa

##

if __name__=="__main__" :
    with Session(engine) as se:
        # 9b3d8156-50c0-4924-bd57-df7a59c443d2
        l_atrib : list[Item] = se.exec(select(Item).where(Item.oid=="9b3d8156-50c0-4924-bd57-df7a59c443d2").order_by(Item.oid)).all()
        clazz = eval("Pessoa")
        saved=clazz()
        for item in l_atrib :
            setattr(saved, item.key, item.value)
                    
        print("classe: ", saved.__class__.__name__, " obj: ", saved)