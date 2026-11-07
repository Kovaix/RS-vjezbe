# backend_app – REST API (FastAPI)

**Javni URL (Render web servis):** https://UPISI-SVOJ-URL.onrender.com
**Interaktivna dokumentacija (Swagger):** https://UPISI-SVOJ-URL.onrender.com/docs

## Endpointi

| Metoda | Putanja | Opis | Uspješan status |
|---|---|---|---|
| GET | `/` | informacije o servisu | 200 |
| GET | `/health` | health check | 200 |
| GET | `/jelovnik` | cijeli jelovnik (opcionalno `?kategorija=desert`) | 200 |
| GET | `/jelovnik/{id}` | jedno jelo (404 ako ne postoji) | 200 |
| GET | `/narudzbe` | sve narudžbe | 200 |
| POST | `/narudzbe` | nova narudžba, JSON: `{"jelo_id": 1, "kolicina": 2}` | 201 |
| DELETE | `/narudzbe/{id}` | brisanje narudžbe | 204 |

## Lokalno pokretanje

```bash
python -m venv .venv
source .venv/bin/activate        # Windows (PowerShell): .venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload        # http://localhost:8000/docs
```

## Render postavke (New → Web Service)

- Root Directory: `vjezbe_1/backend_app`
- Language: `Python 3`
- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- Instance type: Free

## Testiranje

- CLI: `bash zahtjevi_curl.sh https://UPISI-SVOJ-URL.onrender.com`
- GUI: uvezi `postman_kolekcija.json` u Postman i postavi varijablu `base_url`
