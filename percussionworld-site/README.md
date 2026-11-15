# Percussion World — nieuwe website Michel Mordant

Vernieuwde versie van www.percussionworld.nl: dezelfde inhoud en foto's, professioneel herschreven en vormgegeven, in drie talen — **Nederlands (hoofdtaal), Engels en Duits** — met een taalkeuzemenu rechtsboven.

## Mappen

| Map / bestand | Inhoud |
|---|---|
| `site/` | **De kant-en-klare website. Alleen deze map gaat online.** Nederlands in de hoofdmap, Engels in `site/en/`, Duits in `site/de/`; `assets/` (opmaak) en `media/` (foto's, partituren, documenten). De losse bestanden met oude namen (zoals `me.html`, `PAS.htm`) verwijzen bezoekers van oude adressen door. |
| `HANDLEIDING-ONLINE-ZETTEN.md` | Stappenplan om de site op percussionworld.nl te plaatsen |
| `ONTBREKENDE-BESTANDEN.md` | Overzicht van bestanden die op de oude site al kapot waren en nog aangeleverd kunnen worden |
| `INVENTARIS-OUDE-SITE.md` | Alle oude pagina's, knoppen en links, en waar ze nu staan |
| `niet-online/` | Familie- en privéfoto's van de oude site die bewust niet online staan |
| `_src/` | Bronbestanden en bouwscript (zie hieronder) |
| `_preview/` | Schermafbeeldingen |

## Bekijken

Open `site/index.html` in een browser.

## Bouwen (alleen nodig na wijzigingen)

```
pip install pillow beautifulsoup4
python3 _src/build.py
```

- `_src/pages/*.html` — inhoud per pagina (brontekst Engels; de projectpagina's Nederlands of Duits)
- `_src/i18n/<pagina>.txt` — de vertalingen per tekstblok; `_src/i18n/segments/` bevat de genummerde bronteksten
- `_src/glossary.txt` — woordenlijst waarmee uitslagen, instrumentlijsten en data automatisch worden vertaald
- `_src/texts.py` — menu, voettekst en de doorverwijzingen van oude adressen
- Na een wijziging in een brontekst: `python3 _src/build.py --extract` (nummert nieuwe tekstblokken), vertaling toevoegen, daarna `python3 _src/build.py`

## Nog na te lopen door de eigenaar

- **Vaktermen in de vertaling.** Concoursniveaus zijn vertaald als afdeling/divisie (NL) en Stufe/Division (DE). Klopt een term niet met wat de bonden gebruiken, dan is dat op één plek aan te passen (`_src/glossary.txt`).
- **Foto's en namen van kinderen.** Op de foto-, project- en resultatenpagina's staan (zoals op de oude site) herkenbare kinderen en volledige namen van minderjarige leerlingen. Controleer of daar toestemming voor is; in Duitsland (DSGVO) en Nederland (AVG) is die vereist.
- **Woonadres en telefoonnummer** staan nu op de contactpagina (overgenomen van het Stomp-informatieblad op de oude site). Eenvoudig weg te halen als dat de voorkeur heeft.
