// Klijentska strana: šalje HTTP zahtjeve prema REST API-ju i prikazuje odgovore.

const elJelovnik = document.getElementById("jelovnik");
const elNarudzbe = document.getElementById("narudzbe");
const elStatus = document.getElementById("status-api");
const elZapisnik = document.getElementById("zapisnik");
const elFilter = document.getElementById("filter-kategorija");

// Jedna funkcija za sve zahtjeve: šalje zahtjev, zapisuje metodu/putanju/status,
// i vraća JSON (ili null ako odgovor nema tijelo, npr. 204 No Content).
async function posaljiZahtjev(metoda, putanja, tijelo) {
  const opcije = { method: metoda, headers: {} };
  if (tijelo !== undefined) {
    opcije.headers["Content-Type"] = "application/json";
    opcije.body = JSON.stringify(tijelo);
  }

  const pocetak = performance.now();
  try {
    const odgovor = await fetch(API_URL + putanja, opcije);
    const trajanje = Math.round(performance.now() - pocetak);
    zapisi(metoda, putanja, `${odgovor.status} ${odgovor.statusText}`, trajanje, odgovor.ok);

    if (!odgovor.ok) {
      const greska = await odgovor.json().catch(() => ({}));
      throw new Error(greska.detail || `HTTP ${odgovor.status}`);
    }
    return odgovor.status === 204 ? null : await odgovor.json();
  } catch (e) {
    if (e instanceof TypeError) {
      // TypeError od fetch() = mrežna greška ili CORS blokada (nema HTTP statusa)
      zapisi(metoda, putanja, "mrežna greška / CORS", Math.round(performance.now() - pocetak), false);
    }
    throw e;
  }
}

function zapisi(metoda, putanja, status, ms, uspjeh) {
  const li = document.createElement("li");
  li.className = uspjeh ? "ok" : "greska";
  li.textContent = `${metoda} ${putanja} → ${status} (${ms} ms)`;
  elZapisnik.prepend(li);
}

const eura = (x) => x.toLocaleString("hr-HR", { style: "currency", currency: "EUR" });

// ---------- GET /health ----------
async function provjeriApi() {
  // Render besplatni plan "uspava" servis nakon 15 min; prvi zahtjev može trajati ~1 min.
  const timer = setTimeout(() => {
    elStatus.textContent = "Poslužitelj se budi (Render free plan) – pričekaj do minutu…";
  }, 3000);
  try {
    await posaljiZahtjev("GET", "/health");
    elStatus.textContent = `Povezano s ${API_URL}`;
    elStatus.className = "status ok";
    return true;
  } catch (e) {
    elStatus.textContent = `Ne mogu se spojiti na ${API_URL} (${e.message}). Provjeri API_URL u config.js.`;
    elStatus.className = "status greska";
    return false;
  } finally {
    clearTimeout(timer);
  }
}

// ---------- GET /jelovnik?kategorija=... ----------
async function ucitajJelovnik() {
  const kat = elFilter.value;
  const putanja = kat ? `/jelovnik?kategorija=${encodeURIComponent(kat)}` : "/jelovnik";
  const jela = await posaljiZahtjev("GET", putanja);

  elJelovnik.innerHTML = "";
  for (const jelo of jela) {
    const li = document.createElement("li");
    li.innerHTML = `
      <div><strong>${jelo.naziv}</strong><span class="oznaka">${jelo.kategorija}</span></div>
      <div class="desno">
        <span>${eura(jelo.cijena)}</span>
        <input type="number" min="1" max="20" value="1" aria-label="Količina" />
        <button>Naruči</button>
      </div>`;
    const kolicina = li.querySelector("input");
    li.querySelector("button").addEventListener("click", () => naruci(jelo.id, Number(kolicina.value)));
    elJelovnik.append(li);
  }
}

// ---------- POST /narudzbe ----------
async function naruci(jeloId, kolicina) {
  try {
    await posaljiZahtjev("POST", "/narudzbe", { jelo_id: jeloId, kolicina });
    await ucitajNarudzbe();
  } catch (e) {
    alert("Narudžba nije uspjela: " + e.message);
  }
}

// ---------- GET /narudzbe ----------
async function ucitajNarudzbe() {
  const narudzbe = await posaljiZahtjev("GET", "/narudzbe");
  elNarudzbe.innerHTML = "";
  if (narudzbe.length === 0) {
    elNarudzbe.innerHTML = `<li class="prazno">Još nema narudžbi.</li>`;
    return;
  }
  for (const n of narudzbe) {
    const li = document.createElement("li");
    li.innerHTML = `
      <div>#${n.id} · ${n.naziv_jela} × ${n.kolicina}</div>
      <div class="desno"><span>${eura(n.ukupno)}</span><button class="sekundarni">Obriši</button></div>`;
    li.querySelector("button").addEventListener("click", () => obrisi(n.id));
    elNarudzbe.append(li);
  }
}

// ---------- DELETE /narudzbe/{id} ----------
async function obrisi(id) {
  await posaljiZahtjev("DELETE", `/narudzbe/${id}`);
  await ucitajNarudzbe();
}

// ---------- Pokretanje ----------
elFilter.addEventListener("change", ucitajJelovnik);

(async () => {
  if (await provjeriApi()) {
    await ucitajJelovnik();
    await ucitajNarudzbe();
  }
})();
