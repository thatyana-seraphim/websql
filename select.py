from fastapi import FastAPI, Query
import pandas as pd

app = FastAPI()

# Base simulada
data = [
    {"nome": "Ana", "idade": 20, "cidade": "SP"},
    {"nome": "Bruno", "idade": 17, "cidade": "RJ"},
    {"nome": "Carlos", "idade": 25, "cidade": "SP"},
    {"nome": "Diana", "idade": 30, "cidade": "RJ"},
    {"nome": "Eduardo", "idade": 40, "cidade": "MG"},
]

df = pd.DataFrame(data)


# -----------------------------
# Parser de WHERE
# -----------------------------
def apply_where(df, where: str):
    if not where:
        return df

    field, op, value = where.split(".")

    value = int(value)

    if op == "gt":
        return df[df[field] > value]
    elif op == "lt":
        return df[df[field] < value]
    elif op == "eq":
        return df[df[field] == value]
    else:
        return df


# ----------------------------- 
# Parser de SELECT + GROUP BY
# -----------------------------
def apply_select_groupby(df, select: str, groupby: str):
    if not select:
        return df

    fields = select.split(",")

    agg = {}
    normal_fields = []

    for f in fields:
        if f.startswith("count."):
            col = f.split(".")[1]
            agg[col] = "count"
        else:
            normal_fields.append(f)

    if groupby:
        grouped = df.groupby(groupby)

        result = grouped.agg(agg).reset_index()

        return result

    return df[normal_fields]


# -----------------------------
# Endpoint principal
# -----------------------------
@app.get("/pastas/{entidade}")
def query(
    entidade: str,
    select: str = Query(None),
    where: str = Query(None),
    groupby: str = Query(None),
):
    result = df.copy()

    # WHERE
    result = apply_where(result, where)

    # SELECT + GROUPBY
    result = apply_select_groupby(result, select, groupby)

    return result.to_dict(orient="records")