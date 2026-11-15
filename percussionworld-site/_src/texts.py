"""Vaste teksten, menu, doorverwijzingen en woordenlijst voor build.py."""

NAV = [
    ("about", "about.html", {"nl": "Over Michel", "en": "About", "de": "Über Michel"}),
    ("compositions", "compositions.html", {"nl": "Composities", "en": "Compositions", "de": "Kompositionen"}),
    ("teaching", "teaching.html", {"nl": "Lesgeven", "en": "Teaching", "de": "Unterricht"}),
    ("ensembles", "ensembles.html", {"nl": "Ensembles", "en": "Ensembles", "de": "Ensembles"}),
    ("projects", "projects.html", {"nl": "Projecten", "en": "Projects", "de": "Projekte"}),
    ("adjudication", "adjudication.html", {"nl": "Jurering", "en": "Adjudication", "de": "Jury"}),
    ("pas", "pas.html", {"nl": "PAS Nederland", "en": "PAS Netherlands", "de": "PAS Niederlande"}),
    ("photos", "photos.html", {"nl": "Foto’s", "en": "Photos", "de": "Fotos"}),
    ("contact", "contact.html", {"nl": "Contact", "en": "Contact", "de": "Kontakt"}),
]

SOCIAL = [
    ({"nl": "YouTube", "en": "YouTube", "de": "YouTube"}, "http://www.youtube.com/user/percussion1962"),
    ({"nl": "Facebook", "en": "Facebook", "de": "Facebook"}, "http://www.facebook.com/profile.php?id=1799524516"),
    ({"nl": "LinkedIn", "en": "LinkedIn", "de": "LinkedIn"}, "http://nl.linkedin.com/pub/michel-mordant/1a/b85/6b5"),
    ({"nl": "Mijn instrumenten", "en": "My instruments", "de": "Meine Instrumente"}, "https://www.facebook.com/profile.php?id=100063491321111"),
    ({"nl": "Gratis bladmuziek", "en": "Free sheet music", "de": "Kostenlose Noten"}, "https://www.facebook.com/share/j786yi8Zd4By21n5/?mibextid=LQQJ4d"),
]

UI = {
    "nl": dict(
        skip="Naar de inhoud", nav_label="Hoofdmenu", menu="Menu", language="Taal", choose_language="Taal kiezen",
        explore="Ontdek", connect="Volg", links="Slagwerklinks", copyright="Copyright",
        close="Sluiten", prev="Vorige", next="Volgende",
        footer_about="Slagwerker, componist, dirigent en slagwerkdocent, werkzaam in Nederland en Duitsland.",
        footer_rights="Alle muziek op deze site &copy; M. Mordant &middot; geregistreerd bij B.U.M.A., Nederland &middot; uitsluitend ter informatie.",
        keywords="slagwerk, percussie, drumband, slagwerkmuziek, componist, dirigent, Mordant, marimba, vibrafoon, xylofoon, drumstel, kleine trom, pauken, slagwerkdocent",
    ),
    "en": dict(
        skip="Skip to content", nav_label="Main", menu="Menu", language="Language", choose_language="Choose language",
        explore="Explore", connect="Connect", links="Percussion links", copyright="Copyright",
        close="Close", prev="Previous", next="Next",
        footer_about="Percussionist, composer, conductor and percussion teacher, working in the Netherlands and Germany.",
        footer_rights="All music on this site &copy; M. Mordant &middot; registered with B.U.M.A., the Netherlands &middot; for information use only.",
        keywords="percussion, drumband, percussion music, composer, conductor, Mordant, marimba, vibraphone, xylophone, drumset, snare drum, timpani, percussion teacher",
    ),
    "de": dict(
        skip="Zum Inhalt", nav_label="Hauptmenü", menu="Menü", language="Sprache", choose_language="Sprache wählen",
        explore="Entdecken", connect="Folgen", links="Schlagzeug-Links", copyright="Urheberrecht",
        close="Schließen", prev="Zurück", next="Weiter",
        footer_about="Schlagzeuger, Komponist, Dirigent und Schlagzeuglehrer, tätig in den Niederlanden und in Deutschland.",
        footer_rights="Alle Musik auf dieser Website &copy; M. Mordant &middot; registriert bei B.U.M.A., Niederlande &middot; nur zur Information.",
        keywords="Schlagzeug, Percussion, Trommelkorps, Schlagzeugmusik, Komponist, Dirigent, Mordant, Marimba, Vibraphon, Xylophon, Drumset, kleine Trommel, Pauken, Schlagzeuglehrer",
    ),
}

# Oude adressen van de vorige website -> nieuwe pagina (zodat Google-resultaten en bladwijzers blijven werken)
REDIRECTS = {
    "frame1.htm": "index.html", "frame2.htm": "index.html",
    "me.html": "about.html", "mmohnen.htm": "church-bells.html",
    "percussionmusic.html": "compositions.html", "notes.html": "compositions.html#drumset",
    "notes2.html": "compositions.html#keyboard", "notes3.html": "compositions.html#snare",
    "notes4.html": "compositions.html#ensemble", "tympani.html": "compositions.html#timpani",
    "whatsnew.html": "compositions.html#recordings", "cd.html": "compositions.html#recordings",
    "focus.html": "compositions.html#keyboard", "focus2.html": "compositions.html#keyboard",
    "focus3.html": "compositions.html#keyboard", "inminiature.html": "compositions.html#keyboard",
    "diph.html": "compositions.html#keyboard", "ediths.html": "compositions.html#snare",
    "tims.html": "compositions.html#snare", "tomstympani.html": "compositions.html#timpani",
    "bermuda.html": "compositions.html#ensemble", "marry.html": "compositions.html#ensemble",
    "shadow.html": "compositions.html#ensemble", "oliver.html": "compositions.html#drumset",
    "myrthehp.html": "compositions.html#drumset",
    "fotos.html": "photos.html", "recensie22032001.html": "photos.html",
    "teachpup.html": "students.html", "teach.html": "teaching.html",
    "drumteach.html": "teaching.html#drumset", "marimbateach.html": "teaching.html#marimba",
    "Snaredrumteaching.html": "teaching.html#snare", "vibrateach.html": "teaching.html#vibraphone",
    "Timpaniteach.html": "teaching.html#timpani", "methodesnare1ejaar.htm": "teaching.html#progress",
    "methodesnare2ejaar.htm": "teaching.html#progress",
    "startmet.html": "start-methods.html", "moisy.html": "start-methods.html#drums",
    "infolinks.html": "links.html", "musicpri.html": "copyright.html", "jury.html": "adjudication.html",
    "Diversen.html": "projects.html#activities", "advert slagwerkkrant.htm": "projects.html#slagwerkkrant",
    "WORKSHOP percussie.htm": "project-workshop-percussie.html", "Stomp in de School.htm": "project-stomp-school.html",
    "Stomp in Schule D.htm": "project-stomp-schule.html", "Kindergarten.htm": "project-kindergarten.html",
    "Klangforscher.htm": "project-klanggarten.html",
    "PAS.htm": "pas.html", "pas2012.htm": "pas.html#dop-2012", "pas2015.htm": "pas.html#dop-2015",
    "pas2018.htm": "pas.html#dop-2018", "pas2020.htm": "pas.html#dop-2020", "pas2022.htm": "pas.html#dop-2022",
    "pas2023.htm": "pas.html#dop-2023",
    "concerts.html": "ensembles.html", "teachdrumband.html": "ensembles.html",
    "wilhelmina.html": "ensembles.html#wilhelmina", "pieter.html": "ensembles.html#st-pieter",
    "eschweiler.html": "ensemble-eschweiler.html", "Drumming.htm": "ensemble-eschweiler.html",
    "recensie01022000.html": "ensemble-eschweiler.html", "recensie061996.html": "ensemble-eschweiler.html",
    "recensie07112000.html": "ensemble-eschweiler.html", "recensie08112000.html": "ensemble-eschweiler.html",
    "recensie28012000.html": "ensemble-eschweiler.html",
    "Heinsberg.html": "ensemble-heinsberg.html", "Gangelt.html": "ensemble-gangelt.html",
    "ceciliaS.html": "ensemble-broeksittard.html", "cecilia.html": "ensemble-grevenbicht.html",
    "limbricht.html": "ensemble-limbricht.html", "kreato.html": "ensemble-kreato.html",
    "concordia.html": "ensemble-einighausen.html", "stephanus.html": "ensemble-dieteren.html",
    "vijlen.html": "ensemble-vijlen.html", "heerlen.html": "ensemble-heerlen.html",
    "schinveld.html": "ensemble-schinveld.html", "recensie291298.html": "ensemble-schinveld.html",
    "noorbeek.html": "ensemble-noorbeek.html", "merkelbeek.htm": "ensemble-merkelbeek.html",
    "cats.html": "ensemble-young-jazz-cats.html",
}

# Woordenlijst voor uitslagen, data en lijsten: zie glossary.txt (Engels | Nederlands | Duits)
from pathlib import Path

GLOSSARY = [
    tuple(line.rsplit("|", 2))
    for line in (Path(__file__).parent / "glossary.txt").read_text(encoding="utf-8").splitlines()
    if line.strip() and not line.startswith("#")
]
