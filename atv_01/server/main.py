from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
import pandas as pd
import asyncio

app = FastAPI()
CSV_PATH = "../../csv/produtos.csv"

lock = asyncio.Lock()

produtos_df = pd.read_csv(CSV_PATH)

class Produto(BaseModel):
    nome: str
    categoria: str
    preco: float


@app.post("/produtos")
async def criar_produtos(produto: Produto):
    global produtos_df
    
    async with lock:
        novo_id = int(produtos_df["id"].max()) + 1 if not produtos_df.empty else 1

        novo_produto = {
            "id": novo_id,
            "nome": produto.nome,
            "categoria": produto.categoria,
            "preco": produto.preco
        }
        
        produtos_df = pd.concat([produtos_df, pd.DataFrame([novo_produto])], ignore_index=True)
        produtos_df.to_csv(CSV_PATH, index=False)

        return {
            "mensagem": "Produto criado com sucesso!",
            "produto": novo_produto
        }

@app.get("/produtos")
async def listar_produtos():
    async with lock:
        return produtos_df.to_dict(orient="records")

@app.get("/produtos/max")
async def max_produto():
    global produtos_df
    async with lock:
        if produtos_df.empty:
            raise HTTPException(404, detail="Não há produtos cadastrados.")
            
        idx_max = produtos_df["preco"].idxmax()
        produto_max = produtos_df.loc[idx_max]
        
        return {
            "id": int(produto_max["id"]),
            "nome": produto_max["nome"],
            "preco": float(produto_max["preco"])
        }

@app.get("/produtos/min")
async def min_produto():
    global produtos_df
    async with lock:
        if produtos_df.empty:
            raise HTTPException(404, detail="Não há produtos cadastrados.")

        idx_min = produtos_df["preco"].idxmin()
        produto_min = produtos_df.loc[idx_min]
        
        return {
            "id": int(produto_min["id"]),
            "nome": produto_min["nome"],
            "preco": float(produto_min["preco"])
        }

@app.get("/produtos/mean")
async def mean():
    global produtos_df
    async with lock:
        if produtos_df.empty:
            return {"Mensagem": "Não há produtos para calcular a média."}

        mean_val = produtos_df["preco"].mean()
        return {
            "Mensagem": f"média dos produtos {mean_val:.2f}"
        }
    
@app.get("/produtos/acima_media")
async def over_mean():
    global produtos_df
    async with lock:
        if produtos_df.empty:
            return []
            
        mean = produtos_df["preco"].mean()
        over = produtos_df[produtos_df["preco"] >= mean]
        return over.to_dict(orient="records")

@app.get("/produtos/abaixo_media")
async def under_mean():
    global produtos_df
    async with lock:
        if produtos_df.empty:
            return []
            
        mean = produtos_df["preco"].mean()
        under = produtos_df[produtos_df["preco"] < mean]
        return under.to_dict(orient="records")

@app.get("/produtos/{id}")
async def obter_produto(id: int):
    global produtos_df
    async with lock:
        filtro = produtos_df["id"] == id
        produto = produtos_df[filtro]
        
        if produto.empty:
            raise HTTPException(404, detail="Produto nao encontrado")
        
        return produto.to_dict(orient="records")[0]

@app.put("/produtos/{id}")
async def atualizar_produto(id: int, produto: Produto):
    global produtos_df
    async with lock:
        produto_antigo = produtos_df.index[produtos_df["id"] == id]

        if produto_antigo.empty:
            raise HTTPException(404, detail="Erro ao tentar atualizar produto")
        
        produtos_df.loc[produto_antigo, ["nome", "categoria", "preco"]] = [produto.nome, produto.categoria, produto.preco]
        produtos_df.to_csv(CSV_PATH, index=False)

        return {
            "mensagem": "Produto atualizado com sucesso",
            "produto": produtos_df.loc[produto_antigo].to_dict(orient="records")[0]
        }

@app.delete("/produtos/{id}")
async def deletar_produto(id: int):
    global produtos_df
    async with lock:
        produto_deletado = produtos_df.index[produtos_df["id"] == id]
        
        if produto_deletado.empty:
            raise HTTPException(404, detail="Produto nao encontrado")
            
        produtos_df = produtos_df.drop(produto_deletado).reset_index(drop=True)
        produtos_df.to_csv(CSV_PATH, index=False)
        
        return {
            "mensagem": f"Produto com o id: {id}, deletado com sucesso!"
        }