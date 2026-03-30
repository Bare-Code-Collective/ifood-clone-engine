from fastapi import FastAPI

app = FastAPI(title="Baré iFood Engine")

@app.get("/")
def read_root():
    return {"status": "Online", "message": "Baré Code Collective no comando!"}

@app.get("/saudacao")
def saudacao_local():
    return {"msg": "Fala, Baré! API rodando direto de Manaus."}