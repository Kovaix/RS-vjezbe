# frontend_app – statična HTML/CSS/JS stranica

**Javni URL (Render static site):** https://UPISI-SVOJ-URL.onrender.com

Klijent koji putem `fetch()` šalje HTTP zahtjeve (GET, POST, DELETE) na `backend_app`.
URL backenda podešava se u `config.js`.

## Datoteke

- `index.html` – struktura stranice (ulazna točka koju Render poslužuje)
- `style.css` – izgled
- `config.js` – `API_URL` backenda
- `app.js` – logika: slanje zahtjeva i prikaz odgovora

## Lokalno pokretanje

```bash
python -m http.server 5500       # pa otvori http://localhost:5500
```

## Render postavke (New → Static Site)

- Root Directory: `vjezbe_1/frontend_app`
- Build Command: `echo "Nema build koraka"`
- Publish Directory: `.`
