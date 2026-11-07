# Vježba 1 – Klijent-poslužitelj arhitektura na HTTP-u

Raspodijeljeni sustavi 2026/2027

| Dio | Tehnologija | Render tip | URL |
|---|---|---|---|
| `frontend_app/` (klijent) | HTML/CSS/JS | Static Site | https://UPISI-SVOJ-URL.onrender.com |
| `backend_app/` (poslužitelj) | Python, FastAPI | Web Service | https://UPISI-SVOJ-URL.onrender.com |

```
Preglednik ──GET index.html──▶ Render Static Site (frontend_app)
    │
    └──fetch(): GET /jelovnik, POST /narudzbe…──▶ Render Web Service (backend_app, FastAPI)
                                    ◀── JSON + HTTP status (200, 201, 404…)
```
