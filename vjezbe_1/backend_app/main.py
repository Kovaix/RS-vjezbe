"""
Jednostavan REST API poslužitelj - Raspodijeljeni sustavi, Vježba 1.

Tema: jelovnik restorana (isti primjer kao u uputama: GET /jelovnik).
Podaci se drže u memoriji (Python lista), bez baze podataka.
Napomena: na besplatnom Render planu servis se "uspava" nakon 15 min
neaktivnosti, pa se narudžbe izgube nakon restarta - to je očekivano.
"""

from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(
    title="RS Vježba 1 - Restoran API",
    description="Jednostavan REST API za jelovnik i narudžbe.",
    version="1.0.0",
)

# CORS: frontend je na drugoj domeni (npr. rs-frontend.onrender.com) od backenda
# (npr. rs-backend.onrender.com). Preglednik zbog "same-origin policy" blokira takve
# zahtjeve osim ako poslužitelj u odgovoru ne kaže da ih dopušta.
# Za vježbu dopuštamo sve domene ("*"); u produkciji bi se ovdje upisao točan URL frontenda.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------- Modeli podataka (Pydantic) ----------
# Pydantic automatski validira tijelo zahtjeva: ako klijent pošalje krive podatke,
# FastAPI sam vraća 422 Unprocessable Entity s opisom greške.

class Jelo(BaseModel):
    id: int
    naziv: str
    cijena: float
    kategorija: str


class NovaNarudzba(BaseModel):
    jelo_id: int
    kolicina: int = Field(default=1, ge=1, le=20)
    napomena: str | None = None


class Narudzba(NovaNarudzba):
    id: int
    naziv_jela: str
    ukupno: float
    vrijeme: str


# ---------- "Baza podataka" u memoriji ----------

JELOVNIK: list[Jelo] = [
    Jelo(id=1, naziv="Fuži s tartufima", cijena=14.50, kategorija="glavno jelo"),
    Jelo(id=2, naziv="Riblja juha", cijena=6.00, kategorija="predjelo"),
    Jelo(id=3, naziv="Ćevapi s ajvarom", cijena=11.00, kategorija="glavno jelo"),
    Jelo(id=4, naziv="Palačinke s orasima", cijena=5.50, kategorija="desert"),
    Jelo(id=5, naziv="Rapska torta", cijena=4.50, kategorija="desert"),
]

NARUDZBE: list[Narudzba] = []
sljedeci_id = 1  # brojač, da se ID ne ponovi nakon brisanja


def pronadi_jelo(jelo_id: int) -> Jelo:
    for jelo in JELOVNIK:
        if jelo.id == jelo_id:
            return jelo
    raise HTTPException(status_code=404, detail=f"Jelo s id={jelo_id} ne postoji")


# ---------- Endpointi ----------

@app.get("/")
def pocetna():
    """Osnovne informacije o servisu - korisno za brzu provjeru radi li servis."""
    return {
        "poruka": "Restoran API radi!",
        "dokumentacija": "/docs",
        "endpointi": ["/jelovnik", "/jelovnik/{id}", "/narudzbe", "/health"],
    }


@app.get("/health")
def health():
    """Health check - Render (i drugi cloud servisi) mogu ovime provjeravati je li servis živ."""
    return {"status": "ok", "vrijeme": datetime.now(timezone.utc).isoformat()}


@app.get("/jelovnik", response_model=list[Jelo])
def dohvati_jelovnik(kategorija: str | None = None):
    """GET /jelovnik ili GET /jelovnik?kategorija=desert (query parametar za filtriranje)."""
    if kategorija:
        return [j for j in JELOVNIK if j.kategorija == kategorija]
    return JELOVNIK


@app.get("/jelovnik/{jelo_id}", response_model=Jelo)
def dohvati_jelo(jelo_id: int):
    """GET /jelovnik/3 - jedno jelo po ID-u (path parametar). Vraća 404 ako ne postoji."""
    return pronadi_jelo(jelo_id)


@app.get("/narudzbe", response_model=list[Narudzba])
def dohvati_narudzbe():
    return NARUDZBE


@app.post("/narudzbe", response_model=Narudzba, status_code=201)
def kreiraj_narudzbu(nova: NovaNarudzba):
    """POST /narudzbe s JSON tijelom {"jelo_id": 1, "kolicina": 2}. Vraća 201 Created."""
    global sljedeci_id
    jelo = pronadi_jelo(nova.jelo_id)
    narudzba = Narudzba(
        id=sljedeci_id,
        naziv_jela=jelo.naziv,
        ukupno=round(jelo.cijena * nova.kolicina, 2),
        vrijeme=datetime.now(timezone.utc).isoformat(),
        **nova.model_dump(),
    )
    NARUDZBE.append(narudzba)
    sljedeci_id += 1
    return narudzba


@app.delete("/narudzbe/{narudzba_id}", status_code=204)
def obrisi_narudzbu(narudzba_id: int):
    """DELETE /narudzbe/1 - vraća 204 No Content (uspjeh, bez tijela odgovora)."""
    for i, n in enumerate(NARUDZBE):
        if n.id == narudzba_id:
            NARUDZBE.pop(i)
            return
    raise HTTPException(status_code=404, detail=f"Narudžba s id={narudzba_id} ne postoji")
