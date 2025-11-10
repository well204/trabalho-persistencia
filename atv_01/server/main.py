from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
import pandas as pd

app = FastAPI()
CSV_PATH = "../../csv/produtos.csv"

produtos_df = pd.read_csv(CSV_PATH)

class Produto(BaseModel):
    nome: str
    categoria: str
    preco: float


@app.post("/produtos")
def criar_produtos(produto: Produto):
    global produtos_df

    novo_id = int(produtos_df["id"].max()) + 1 if not produtos_df.empty else 1

    novo_produto = {
        "id": novo_id,
        "nome": produto.nome,
        "categoria": produto.categoria,
        "preco": produto.preco
    }

    produtos_df = produtos_df._append(novo_produto, ignore_index = True)
    produtos_df.to_csv(CSV_PATH, index=False)

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
    produtos_df.to_csv(CSV_PATH, index=False)

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
    produtos_df.to_csv(CSV_PATH, index=False)
    return {
        "mensagem": f"Produto com o id: {id}, deletado com sucesso!"
    }