from fastapi import FastAPI

from fluxosolo.routers import auth, transactions, users

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(transactions.router)


@app.get("/")
def read_root():
    return {"message": "Bem vindo ao fluxoSolo"}
