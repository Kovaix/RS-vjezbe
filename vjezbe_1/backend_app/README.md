# Backend

URL: https://rs-vjezbe-trap.onrender.com

Pokretanje lokalno:

```
pip install -r requirements.txt
uvicorn main:app --reload
```

Endpointi:

```
GET /jela
GET /jela/{id}
POST /narudzbe
GET /narudzbe
```

Primjer curl:

```
curl https://rs-vjezbe-trap.onrender.com/jela
curl -X POST https://rs-vjezbe-trap.onrender.com/narudzbe -H "Content-Type: application/json" -d "{\"jelo_id\": 1, \"kolicina\": 2}"
```
