import httpx

BASE_URL = "http://127.0.0.1:8000"


def criar_produto(nome: str, categoria: str, preco: float):
    payload = {"nome": nome, "categoria": categoria, "preco": preco}
    try:
        resp = httpx.post(f"{BASE_URL}/produtos", json=payload)
        print(resp.json())
    except httpx.RequestError as e:
        print(f"Erro ao conectar: {e}")

def listar_produtos():
    try:
        resp = httpx.get(f"{BASE_URL}/produtos")
        print(resp.json())
    except httpx.RequestError as e:
        print(f"Erro ao conectar: {e}")

def obter_produto(id: int):
    try:
        resp = httpx.get(f"{BASE_URL}/produtos/{id}")
        print(resp.json())
    except httpx.RequestError as e:
        print(f"Erro ao conectar: {e}")

def atualizar_produto(id: int, nome: str, categoria: str, preco: float):
    payload = {"nome": nome, "categoria": categoria, "preco": preco}
    try:
        resp = httpx.put(f"{BASE_URL}/produtos/{id}", json=payload)
        print(resp.json())
    except httpx.RequestError as e:
        print(f"Erro ao conectar: {e}")

def deletar_produto(id: int):
    try:
        resp = httpx.delete(f"{BASE_URL}/produtos/{id}")
        print(resp.json())
    except httpx.RequestError as e:
        print(f"Erro ao conectar: {e}")


def max_produto():
    try:
        resp = httpx.get(f"{BASE_URL}/produtos/max")
        print(resp.json())
    except httpx.RequestError as e:
        print(f"Erro ao conectar: {e}")

def min_produto():
    try:
        resp = httpx.get(f"{BASE_URL}/produtos/min")
        print(resp.json())
    except httpx.RequestError as e:
        print(f"Erro ao conectar: {e}")

def mean_produto():
    try:
        resp = httpx.get(f"{BASE_URL}/produtos/mean")
        print(resp.json())
    except httpx.RequestError as e:
        print(f"Erro ao conectar: {e}")
    
def over_mean_produto():
    try:
        resp = httpx.get(f"{BASE_URL}/produtos/acima_media")
        print(resp.json())
    except httpx.RequestError as e:
        print(f"Erro ao conectar: {e}")

def under_mean_produto():
    try:
        resp = httpx.get(f"{BASE_URL}/produtos/abaixo_media")
        print(resp.json())
    except httpx.RequestError as e:
        print(f"Erro ao conectar: {e}")


if __name__ == "__main__":
 

    listar_produtos()
    #obter_produto(1)
    #criar_produto(nome="Notebook", categoria="eletronicos", preco=3500.50)
    #atualizar_produto(id=1, nome="Notebook Gamer", categoria="eletronicos", preco=5500.00) 
    #deletar_produto(1)

     #max_produto()
     #min_produto()
     #mean_produto()
     #over_mean_produto()
     #under_mean_produto()