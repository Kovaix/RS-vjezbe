const API_URL = "https://UPISI-URL-BACKENDA.onrender.com";

async function ucitajJela() {
  const res = await fetch(API_URL + "/jela");
  const jela = await res.json();

  const lista = document.getElementById("jela");
  const select = document.getElementById("jelo");
  lista.innerHTML = "";
  select.innerHTML = "";

  for (const jelo of jela) {
    lista.innerHTML += `<li>${jelo.naziv} - ${jelo.cijena} EUR</li>`;
    select.innerHTML += `<option value="${jelo.id}">${jelo.naziv}</option>`;
  }
}

async function ucitajNarudzbe() {
  const res = await fetch(API_URL + "/narudzbe");
  const narudzbe = await res.json();

  const lista = document.getElementById("narudzbe");
  lista.innerHTML = "";
  for (const n of narudzbe) {
    lista.innerHTML += `<li>Narudžba ${n.id}: jelo ${n.jelo_id}, količina ${n.kolicina}</li>`;
  }
}

async function posaljiNarudzbu(e) {
  e.preventDefault();
  const podaci = {
    jelo_id: Number(document.getElementById("jelo").value),
    kolicina: Number(document.getElementById("kolicina").value),
  };

  await fetch(API_URL + "/narudzbe", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(podaci),
  });
  ucitajNarudzbe();
}

async function start() {
  try {
    await ucitajJela();
    await ucitajNarudzbe();
  } catch (err) {
    document.getElementById("poruka").textContent = "Backend ne radi ili se još budi, probaj za minutu.";
  }
}

document.getElementById("forma").addEventListener("submit", posaljiNarudzbu);
start();
