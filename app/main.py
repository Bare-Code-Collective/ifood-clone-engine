from fastapi import FastAPI

app = FastAPI(
    title="Baré Code Collective - iFood Engine",
    description="API de recomendação e logística para o projeto iFood Clone",
    version="0.1.0"
)

@app.get("/", tags=["Health Check"])
def home():
    return {
        "status": "Online",
        "message": "Baré Code Collective operando direto de Manaus!",
        "versao": "0.1.0"
    }

@app.get("/cardapio-regional", tags=["Mock"])
def buscar_itens_regionais():
    # Isso é apenas um exemplo para testar a rota
    return {
        "restaurante": "Delícias do Amazonas",
        "destaques": ["X-Caboquinho", "Tambaqui Assado", "Suco de Cupuaçu"]
    }