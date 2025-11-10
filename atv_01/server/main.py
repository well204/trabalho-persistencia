from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
import pandas as pd

app = FastAPI()
contador_id = 0

produtos_df = pd.DataFrame (
    {
        "id": [1,2,3],
        "nome": ["tv","smartphone","pc"],
        "categoria": ["eletronico", "eletronico", "eletronico"],
        "preco": [298.98, 4830.30, 3992.30]
    }
)

class Produto(BaseModel):
    nome: str
    categoria: str
    preco: float


@app.post("/produtos")
def criar_produtos(produto: Produto):
    global produtos_df, contador_id

    novo_produto = {
        "id": contador_id,
        "nome": produto.nome,
        "categoria": produto.categoria,
        "preco": produto.preco
    }

    produtos_df = produtos_df._append(novo_produto, ignore_index = True)
    contador_id = contador_id + 1

    return {
        "mensagem": "Produto criado com sucesso!",
        "produto": novo_produto
    }

@app.get("/produtos")
def listar_produtos():
    return produtos_df.to_dict(orient = "records")

@app.get("/produtos/{id}")
def obter_produto(id: int):
    global produtos_df
    filtro = produtos_df["id"] == id

    produto = produtos_df[filtro]
    if produto.empty:
        raise HTTPException(402, detail= "Produto nao encontrado")
    return produto.to_dict(orient = "records")[0]

@app.put("/produtos/{id}")
def atualizar_produto(id: int, produto: Produto):
    global produtos_df
    produto_antigo = produtos_df.index[produtos_df["id"] == id]

    if produto_antigo.empty:
        raise HTTPException(404, detail="Erro ao tentar atualizar produto")
    produtos_df.loc[produto_antigo, ["nome", "categoria", "preco"]] = [produto.nome, produto.categoria, produto.preco]

    return {
        "mensagem": "Produto adicionado com sucesso",
        "produto": produtos_df.loc[produto_antigo].to_dict(orient = "records")[0]
    }

@app.delete("/produtos/{id}")
def deletar_produto(id: int):
    global produtos_df
    produto_deletado = produtos_df.index[produtos_df["id"] == id]
    if produto_deletado.empty:
        raise HTTPException(404, detail= "Produto nao encontrado")
    produtos_df = produtos_df.drop(produto_deletado).reset_index(drop=True)
    return {
        "mensagem": f"Produto com o id: {id}, deletado com sucesso!"
    }