# Stappenplan: de nieuwe site op www.percussionworld.nl zetten

De nieuwe site is een 'statische' website: gewone bestanden (HTML, CSS, foto's), zonder database of beheerpaneel. Online zetten betekent: de inhoud van de map **`site/`** op de webruimte van percussionworld.nl plaatsen, op de plek waar nu de oude site staat. De domeinnaam en het adres veranderen niet.

Reken op ongeveer een half uur. Er gaat niets verloren: in stap 3 maak je eerst een volledige reservekopie van de oude site.

## Wat je nodig hebt

1. **De inloggegevens van de hosting** van percussionworld.nl. De eigenaar heeft ze ooit van zijn hostingbedrijf gekregen; het zijn dezelfde gegevens waarmee hij nu pagina's uploadt:
   - FTP-adres (bijv. `ftp.percussionworld.nl`)
   - gebruikersnaam en wachtwoord
   - Weet hij ze niet meer? Ze staan in het klantenpaneel van het hostingbedrijf (zie de jaarlijkse factuur voor de naam), of de helpdesk kan ze opnieuw verstrekken.
2. **Het programma FileZilla** (gratis): https://filezilla-project.org → 'Download FileZilla Client'. Sommige hostingbedrijven hebben in hun klantenpaneel ook een 'Bestandsbeheer' (File Manager); dat werkt ook, maar FileZilla is handiger voor veel bestanden tegelijk.
3. **De map `site/`** op je eigen computer (stap 1).

## Stap 1 — Download de nieuwe site

1. Ga op GitHub naar de repository `smordant/pws-tool-vwo` en kies de branch `claude/awesome-brahmagupta-90qs9i`.
2. Klik op de groene knop **Code → Download ZIP** en pak het zip-bestand uit.
3. Open de map `percussionworld-site/site/`. **Alleen de inhoud van deze map gaat online** (`index.html`, de mappen `en`, `de`, `assets`, `media` en de overige `.html`/`.htm`-bestanden).

## Stap 2 — Bekijk de site eerst op je eigen computer

Dubbelklik op `site/index.html`. De site opent in je browser. Klik door het menu, wissel rechtsboven van taal (NL / EN / DE) en controleer of alles naar wens is. Wil je nog iets veranderd hebben, dan is dit het moment.

## Stap 3 — Maak een reservekopie van de oude site

1. Open FileZilla. Vul bovenaan in: **Host** (het FTP-adres), **Gebruikersnaam**, **Wachtwoord** en klik op **Snelverbinden**. (Vraagt FileZilla iets over een certificaat: kies 'OK'.)
2. Rechts zie je nu de bestanden op de server. Zoek de map waar de oude site in staat: de map waarin je `index.html`, `frame1.htm` en `frame2.htm` ziet. Vaak heet die `public_html`, `httpdocs`, `www` of `htdocs`; soms is het direct de eerste map.
3. Maak links (jouw computer) een nieuwe map aan, bijvoorbeeld `backup-oude-site-2026`.
4. Selecteer rechts alle bestanden en mappen (Ctrl+A) en sleep ze naar die backupmap links. Wacht tot de wachtrij onderaan leeg is (dit is ongeveer 120 MB en kan enkele minuten duren).
5. Controleer dat de backupmap gevuld is (o.a. `index.html`, `me.html`, `Fotos2.html.mht`). **Bewaar deze map goed** — hiermee kun je de oude site altijd terugzetten.

## Stap 4 — Verwijder de oude bestanden van de server

Selecteer rechts (op de server) de bestanden en mappen van de oude site en verwijder ze (rechtermuisknop → Verwijderen).

**Laat staan** wat niet bij de website hoort, als het er is: bestanden die met een punt beginnen (zoals `.htaccess`), en mappen als `cgi-bin`, `.well-known`, `webmail`, `stats` of `logs`. Bij twijfel: laat het staan; oude losse bestanden zitten de nieuwe site niet in de weg.

*Liever voorzichtig?* Sla deze stap over en upload direct (stap 5): de nieuwe bestanden overschrijven dan de oude met dezelfde naam. Er blijven dan wel ongebruikte oude bestanden op de server staan.

## Stap 5 — Upload de nieuwe site

1. Ga links (jouw computer) naar de map `percussionworld-site/site/`.
2. Selecteer **alles in die map** (Ctrl+A) — dus niet de map `site` zelf, maar de inhoud ervan.
3. Sleep de selectie naar rechts, in de map van stap 3 (waar eerst de oude `index.html` stond). Vraagt FileZilla of bestanden overschreven mogen worden: kies 'Overschrijven' en vink 'Altijd deze actie gebruiken' aan.
4. Wacht tot de wachtrij leeg is (ongeveer 60 MB, bijna 600 bestanden). Staat er onderaan iets op het tabblad **Mislukte overdrachten**? Klik er met rechts op en kies 'Alles opnieuw in wachtrij plaatsen en verwerken'.

Het resultaat op de server: `index.html` staat direct in de hoofdmap van de website, met daarnaast de mappen `assets`, `media`, `en` en `de`.

## Stap 6 — Controleer het resultaat

Open in je browser (gebruik Ctrl+F5 om de oude versie uit het geheugen van de browser te halen):

- [ ] https://www.percussionworld.nl — de nieuwe Nederlandse homepage verschijnt
- [ ] het taalmenu rechtsboven: kies English en Deutsch (`/en/` en `/de/`)
- [ ] https://www.percussionworld.nl/photos.html — foto's laden en vergroten als je erop klikt
- [ ] https://www.percussionworld.nl/me.html — een oud adres; dit springt automatisch door naar de nieuwe pagina 'Over Michel' (zo blijven Google-resultaten en bladwijzers werken)
- [ ] bekijk de site ook even op een telefoon

Zie je nog de oude site? Wacht een paar minuten en ververs opnieuw; anders staat `index.html` waarschijnlijk een map te diep (bijvoorbeeld in `…/site/index.html`). Verplaats dan de inhoud één niveau omhoog.

## Stap 7 — Terugzetten (alleen als het nodig is)

Mocht er iets misgaan: verwijder de geüploade bestanden en sleep de inhoud van je backupmap terug naar de server. De oude site staat er dan weer precies zoals voorheen.

## Later iets wijzigen

- **Tekst aanpassen:** de teksten staan in `_src/pages/` (brontekst) en `_src/i18n/` (vertalingen). Na een wijziging: `python3 _src/build.py` uitvoeren en de gewijzigde bestanden uit `site/` opnieuw uploaden. Het is het eenvoudigst om de wijziging aan mij door te geven; dan lever ik de bijgewerkte map `site/` aan.
- **Ontbrekende foto's toevoegen:** zie `ONTBREKENDE-BESTANDEN.md`.

## Goed om te weten

- De server van percussionworld.nl draait op Linux: hoofdletters in bestandsnamen tellen mee. Hernoem daarom geen bestanden in de map `site/`.
- De site gebruikt lettertypen van Google Fonts. Wil de eigenaar dat (om privacyredenen, met name in Duitsland) liever niet, dan kan ik de lettertypen in de site zelf opnemen.
- Voor Google is geen actie nodig: de zoekmachine pikt de nieuwe pagina's vanzelf op en de oude adressen verwijzen door.
