from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# dopusti zahtjeve s frontenda
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

jela = [
    {"id": 1, "naziv": "Fuži s tartufima", "cijena": 14.5},
    {"id": 2, "naziv": "Riblja juha", "cijena": 6.0},
    {"id": 3, "naziv": "Ćevapi", "cijena": 11.0},
    {"id": 4, "naziv": "Palačinke", "cijena": 5.5},
]

narudzbe = []


class Narudzba(BaseModel):
    jelo_id: int
    kolicina: int


@app.get("/")
def pocetna():
    return {"poruka": "API radi"}


@app.get("/jela")
def sva_jela():
    return jela


@app.get("/jela/{id}")
def jedno_jelo(id: int):
    for jelo in jela:
        if jelo["id"] == id:
            return jelo
    raise HTTPException(status_code=404, detail="Jelo ne postoji")


@app.post("/narudzbe")
def nova_narudzba(narudzba: Narudzba):
    jedno_jelo(narudzba.jelo_id)  # baci 404 ako jelo ne postoji
    nova = {"id": len(narudzbe) + 1, "jelo_id": narudzba.jelo_id, "kolicina": narudzba.kolicina}
    narudzbe.append(nova)
    return nova


@app.get("/narudzbe")
def sve_narudzbe():
    return narudzbe
