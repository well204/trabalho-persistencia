import httpx

BASE_URL = "http://127.0.0.1:8000"

def criar_produto():
    resp = httpx.post(
        f"{BASE_URL}/produtos",
        json= {"nome": "TV", "categoria": "eletronicos", "preco": 1100.76}
    )
    print(resp.json())

def listar_produtos():
    resp = httpx.get(f"{BASE_URL}/produtos")
    print(resp.json())

def obter_produto(id: int):
    resp = httpx.get(f"{BASE_URL}/produtos/{id}")
    print(resp.json())

def deletar_produto(id: int):
    resp = httpx.delete(f"{BASE_URL}/produtos/{id}")
    return resp.json()


if __name__=="__main__":
    listar_produtos()
    obter_produto(3)
    deletar_produto(2)
    print("\n")
    criar_produto()
    listar_produtos()
