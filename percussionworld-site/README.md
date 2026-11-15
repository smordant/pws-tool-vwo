# Percussion World — nieuwe website Michel Mordant

Vernieuwde versie van www.percussionworld.nl: dezelfde inhoud en foto's, professioneel herschreven en opgemaakt.

## Bekijken
Open `index.html` in een browser, of start lokaal een server in deze map:

```
python3 -m http.server 8000
```
en ga naar http://localhost:8000.

## Online zetten
Het is een statische site (HTML/CSS/JS, geen database). Upload de hele inhoud van deze map naar de webhosting van percussionworld.nl, behalve de map `_src/` en de `.md`-bestanden. GitHub Pages of Netlify werkt ook.

## Structuur
- `*.html` — de gebouwde pagina's (35)
- `assets/` — huisstijl (`css/style.css`), lightbox en menu (`js/site.js`), favicon
- `media/` — alle foto's, partituurvoorbeelden, PDF's en documenten van de oude site (grote foto's zijn web-geoptimaliseerd)
- `_src/pages/` — de inhoud per pagina; `_src/build.py` voegt kop, menu en voettekst toe
- `INVENTARIS-OUDE-SITE.md` — overzicht van alle oude pagina's, knoppen, links en kapotte links

## Tekst aanpassen
Pas het bestand in `_src/pages/` aan en draai daarna:

```
python3 _src/build.py
```
(Pillow is nodig: `pip install pillow`.) Menu, voettekst en e-mailadres staan bovenin `_src/build.py`.
