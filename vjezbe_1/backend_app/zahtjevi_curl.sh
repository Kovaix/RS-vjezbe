#!/usr/bin/env bash
# HTTP zahtjevi prema deployanom servisu pomoću curl-a (CLI HTTP klijent).
# Pokretanje:  bash zahtjevi_curl.sh https://TVOJ-BACKEND.onrender.com
# -i  = ispiši i zaglavlja odgovora (status line, content-type...)
# -X  = HTTP metoda;  -H = zaglavlje zahtjeva;  -d = tijelo zahtjeva

URL="${1:-http://localhost:8000}"

echo "=== 1) GET / ==="
curl -i "$URL/"
echo -e "\n\n=== 2) GET /jelovnik ==="
curl -i "$URL/jelovnik"
echo -e "\n\n=== 3) GET /jelovnik?kategorija=desert (query parametar) ==="
curl -i "$URL/jelovnik?kategorija=desert"
echo -e "\n\n=== 4) GET /jelovnik/3 (path parametar) ==="
curl -i "$URL/jelovnik/3"
echo -e "\n\n=== 5) GET /jelovnik/99 (očekujemo 404 Not Found) ==="
curl -i "$URL/jelovnik/99"
echo -e "\n\n=== 6) POST /narudzbe (očekujemo 201 Created) ==="
curl -i -X POST "$URL/narudzbe" -H "Content-Type: application/json" -d '{"jelo_id": 1, "kolicina": 2, "napomena": "bez luka"}'
echo -e "\n\n=== 7) POST /narudzbe s neispravnim podacima (očekujemo 422) ==="
curl -i -X POST "$URL/narudzbe" -H "Content-Type: application/json" -d '{"jelo_id": "abc"}'
echo -e "\n\n=== 8) GET /narudzbe ==="
curl -i "$URL/narudzbe"
echo
