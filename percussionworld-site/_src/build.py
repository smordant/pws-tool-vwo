#!/usr/bin/env python3
"""Bouwt de drietalige website Percussion World (Nederlands, Engels, Duits).

Gebruik:
    python3 _src/build.py               # bouwt site/ (nl), site/en/ en site/de/
    python3 _src/build.py --extract     # werkt de lijst met te vertalen teksten bij
    python3 _src/build.py --mirror PAD  # vult site/media/ opnieuw vanuit een kopie van de oude site

Hoe het werkt
* De inhoud van elke pagina staat in _src/pages/<pagina>.html (brontaal Engels,
  tenzij bovenaan `<!-- lang: nl -->` of `<!-- lang: de -->` staat).
* Elke tekst op een pagina is een "segment". _src/i18n/segments/<pagina>.txt bevat
  per regel `nummer<TAB>brontekst`; _src/i18n/<pagina>.txt bevat de vertalingen:
        12
        nl: Nederlandse tekst
        de: Deutscher Text
  Binnen een segment staan <1>...</1>, <2>...</2> voor links/cursief e.d.
* Segmenten zonder eigen vertaling (uitslagen, data, namen) worden met de
  woordenlijst GLOSSARY omgezet.
* {{m:bestand}} verwijst naar een bestand in site/media/.

Nodig: pip install pillow beautifulsoup4
"""
import html
import re
import shutil
import sys
from pathlib import Path

from bs4 import BeautifulSoup, Comment, NavigableString, Tag
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "_src" / "pages"
I18N = ROOT / "_src" / "i18n"
SEGDIR = I18N / "segments"
SITE = ROOT / "site"
MEDIA = SITE / "media"
MIRROR = Path(sys.argv[sys.argv.index("--mirror") + 1]) if "--mirror" in sys.argv else None
EXTRACT = "--extract" in sys.argv
MAX_SIDE = 1800
LANGS = ["nl", "en", "de"]
LANG_NAMES = {"nl": "Nederlands", "en": "English", "de": "Deutsch"}
DOMAIN = "https://www.percussionworld.nl"
EMAIL = "percussion@home.nl"
WEBMASTER = "Sander Mordant"  # websitebouwer en -beheerder (voettekst)
WEBMASTER_EMAIL = "sandermordant.web@outlook.com"
CUR_PAGE = ' aria-current="page"'
CUR_LANG = ' aria-current="true"'

sys.path.insert(0, str(ROOT / "_src"))
from texts import GLOSSARY, NAV, REDIRECTS, SOCIAL, UI  # noqa: E402

# ---------------------------------------------------------------- media
media_map = {}
missing = []


def slug(rel):
    rel = rel.replace("_bestanden/", "-").replace("/", "-")
    stem, _, ext = rel.rpartition(".")
    stem = re.sub(r"[^a-z0-9]+", "-", stem.lower()).strip("-")
    return f"{stem}.{ext.lower()}"


def find_source(rel):
    """Zoek een bestand in de kopie van de oude site; kies Words grotere origineel van een foto."""
    src = MIRROR / rel
    m = re.match(r"(.*_bestanden/image)(\d{3})\.(\w+)$", rel)
    if m and src.exists():
        n = int(m.group(2))
        try:
            w, h = Image.open(src).size
        except Exception:
            return src
        for ext in ("jpg", "png", "gif", "jpeg"):
            cand = MIRROR / f"{m.group(1)}{n - 1:03d}.{ext}"
            if cand.exists():
                try:
                    cw, ch = Image.open(cand).size
                except Exception:
                    continue
                if cw > w and abs(cw / ch - w / h) < 0.04:
                    return cand
    return src


def media_url(rel):
    rel = rel.strip()
    if rel in media_map:
        return media_map[rel]
    name = slug(rel)
    ext = name.rsplit(".", 1)[1]
    if MIRROR is None:
        existing = sorted(MEDIA.glob(name.rsplit(".", 1)[0] + ".*"))
        if existing:
            media_map[rel] = f"media/{existing[0].name}"
            return media_map[rel]
        missing.append(rel)
        return "#missing"
    src = find_source(rel)
    if not src.exists():
        missing.append(rel)
        return "#missing"
    MEDIA.mkdir(exist_ok=True)
    if ext in ("jpg", "jpeg", "png", "tif", "tiff", "bmp"):
        im = Image.open(src)
        im.load()
        big = max(im.size) > MAX_SIDE
        has_alpha = im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info)
        heavy_png = src.suffix.lower() == ".png" and src.stat().st_size > 350_000 and not has_alpha
        if big or heavy_png or ext in ("tif", "tiff", "bmp"):
            if big:
                im.thumbnail((MAX_SIDE, MAX_SIDE), Image.LANCZOS)
            if has_alpha or ext in ("tif", "tiff", "bmp"):
                name = name.rsplit(".", 1)[0] + ".png"
                im.save(MEDIA / name, optimize=True)
            else:
                name = name.rsplit(".", 1)[0] + ".jpg"
                im.convert("RGB").save(MEDIA / name, quality=84, optimize=True, progressive=True)
        else:
            name = name.rsplit(".", 1)[0] + src.suffix.lower()
            shutil.copyfile(src, MEDIA / name)
    else:
        shutil.copyfile(src, MEDIA / name)
    media_map[rel] = f"media/{name}"
    return media_map[rel]


# ---------------------------------------------------------------- segments
VOID = {"br", "img", "hr", "wbr"}
ATTRS = ("alt", "data-caption")
LITERAL = {"work-title", "perf-title", "brand-name"}  # titels van stukken: nooit via de woordenlijst


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def is_segment(el):
    return any(isinstance(c, NavigableString) and not isinstance(c, Comment) and c.strip() for c in el.children)


def encode(el, tags):
    out = []
    for c in el.children:
        if isinstance(c, Comment):
            continue
        if isinstance(c, NavigableString):
            out.append(str(c))
        else:
            tags.append(c)
            n = len(tags)
            out.append(f"<{n}/>" if c.name in VOID else f"<{n}>{encode(c, tags)}</{n}>")
    return "".join(out)


def open_tag(t):
    attrs = "".join(
        f' {k}="{html.escape(" ".join(v) if isinstance(v, list) else v, quote=True)}"' for k, v in t.attrs.items()
    )
    return f"<{t.name}{attrs}>"


def decode(text, tags):
    text = text.replace("&", "&amp;")
    text = re.sub(r"<(\d+)/>", lambda m: open_tag(tags[int(m.group(1)) - 1]), text)
    text = re.sub(r"<(\d+)>", lambda m: open_tag(tags[int(m.group(1)) - 1]), text)
    return re.sub(r"</(\d+)>", lambda m: f"</{tags[int(m.group(1)) - 1].name}>", text)


def segments_of(soup):
    """Geeft (element, brontekst, tags) voor elk tekstblok, in documentvolgorde."""
    found = []

    def walk(el):
        for c in list(el.children):
            if not isinstance(c, Tag) or c.name in ("script", "style"):
                continue
            if is_segment(c):
                tags = []
                found.append((c, norm(encode(c, tags)), tags))
            else:
                walk(c)

    walk(soup)
    return found


def has_letters(s):
    return bool(re.search(r"[A-Za-zÀ-ÿ]{2,}", re.sub(r"</?\d+/?>", "", s)))


# ---------------------------------------------------------------- catalogue
def load_catalogue():
    """bron-tekst -> {taal: vertaling}"""
    cat = {}
    for seg_file in sorted(SEGDIR.glob("*.txt")):
        ids = {}
        for line in seg_file.read_text(encoding="utf-8").splitlines():
            if "\t" in line:
                n, src = line.split("\t", 1)
                ids[n] = src
        tr_file = I18N / seg_file.name
        if not tr_file.exists():
            continue
        cur = None
        for ln, line in enumerate(tr_file.read_text(encoding="utf-8").splitlines(), 1):
            line = line.rstrip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("= "):  # letterlijke brontekst in plaats van een nummer
                cur = "=" + line[2:]
                ids[cur] = line[2:]
                continue
            if re.fullmatch(r"\d+", line):
                cur = line
                if cur not in ids:
                    print(f"  ! {tr_file.name}:{ln}: onbekend segment {cur}")
                continue
            m = re.match(r"(nl|en|de): ?(.*)$", line)
            if m and cur in ids:
                cat.setdefault(ids[cur], {})[m.group(1)] = m.group(2)
            elif not m:
                print(f"  ! {tr_file.name}:{ln}: regel niet begrepen: {line[:60]}")
    return cat


def _cap(w):
    return w[:1].upper() + w[1:]


PROTECT = []  # namen die nooit vertaald worden


def compile_glossary():
    """Reguliere expressies eerst (in volgorde), daarna vaste termen van lang naar kort."""
    rx, plain = [], []
    for row in GLOSSARY:
        if row[0] == row[1] == row[2]:
            PROTECT.append(row[0])
        elif row[0].startswith("re:"):
            rx.append((re.compile(row[0][3:]), row[1], row[2]))
        else:
            plain.append(row)
    plain.sort(key=lambda r: -len(r[0]))
    for src, nl, de in plain:
        pat = r"(?<![\w’'])" + re.escape(src) + r"(?![\w’'])"
        rx.append((re.compile(pat), nl, de))
        if src[:1].islower():
            rx.append((re.compile(r"(?<![\w’'])" + re.escape(_cap(src)) + r"(?![\w’'])"), _cap(nl), _cap(de)))
    return rx


GLOSS = compile_glossary()


def glossary(text, lang, tags=()):
    """Vertaal termen; tekst binnen cursief (titels van stukken) blijft ongemoeid."""
    i = {"nl": 1, "de": 2}[lang]
    keep = {str(n + 1) for n, t in enumerate(tags) if t.name in ("em", "i", "cite")}
    parts = re.split(r"(<(\d+)>.*?</\2>)", text) if keep else [text]
    out, k = [], 0
    while k < len(parts):
        chunk = parts[k]
        m = re.match(r"<(\d+)>", chunk) if keep else None
        if m and len(parts) > k + 1 and parts[k + 1] == m.group(1):
            if m.group(1) not in keep:
                for r in GLOSS:
                    chunk = r[0].sub(r[i], chunk)
            out.append(chunk)
            k += 2
            continue
        for n, name in enumerate(PROTECT):
            chunk = chunk.replace(name, f"\x00{n}\x00")
        for r in GLOSS:
            chunk = r[0].sub(r[i], chunk)
        chunk = re.sub("\x00(\\d+)\x00", lambda m: PROTECT[int(m.group(1))], chunk)
        out.append(chunk)
        k += 1
    return "".join(out)


STOP = re.compile(
    r"\b(the|and|with|of|for|from|by|was|were|is|are|his|this|that|their|have|has|into|also|which|who|at|on|in cooperation)\b"
)
untranslated = {l: [] for l in LANGS}


def translate(src, lang, page_lang, cat, page, tags=(), literal=False):
    """Vertaal één segment (of attribuutwaarde)."""
    entry = cat.get(src, {})
    if lang in entry:
        return entry[lang]
    if lang == page_lang or literal or not has_letters(src):
        return src
    if page_lang == "en":
        out = glossary(src, lang, tags)
        plain = re.sub(r"<[^>]+>", " ", out)
        if STOP.search(plain):
            untranslated[lang].append((page, src))
        return out
    untranslated[lang].append((page, src))
    return src


# ---------------------------------------------------------------- page template
def lang_href(lang, cur, name):
    """Relatieve link van een pagina in taal `cur` naar dezelfde pagina in taal `lang`."""
    up = "" if cur == "nl" else "../"
    return up + ("" if lang == "nl" else lang + "/") + name


def render(lang, name, meta, body):
    ui = UI[lang]
    pre = "" if lang == "nl" else "../"
    nav_key = meta.get("nav", "none")
    title = meta["title"]
    full_title = f"Michel Mordant — Percussion World" if nav_key == "home" else f"{title} · Michel Mordant"
    desc = html.escape(meta["description"], quote=True)
    nav_items = "\n".join(
        f'        <li><a href="{href}"{CUR_PAGE if key == nav_key else ""}>{labels[lang]}</a></li>'
        for key, href, labels in NAV
    )
    explore = "\n".join(f'<li><a href="{href}">{labels[lang]}</a></li>' for key, href, labels in NAV if key != "contact")
    social = "\n".join(
        f'<li><a href="{u}" target="_blank" rel="noopener">{labels[lang]}</a></li>' for labels, u in SOCIAL
    )
    alternates = "\n".join(
        f'<link rel="alternate" hreflang="{l}" href="{DOMAIN}/{"" if l == "nl" else l + "/"}{"" if name == "index.html" else name}">'
        for l in LANGS
    ) + f'\n<link rel="alternate" hreflang="x-default" href="{DOMAIN}/{"" if name == "index.html" else name}">'
    lang_links = "".join(
        f'<li><a href="{lang_href(l, lang, name)}" hreflang="{l}" lang="{l}"{CUR_LANG if l == lang else ""}>'
        f'<span class="lang-code">{l.upper()}</span>{LANG_NAMES[l]}</a></li>'
        for l in LANGS
    )
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(full_title)}</title>
<meta name="description" content="{desc}">
<meta name="keywords" content="{ui['keywords']}">
<meta property="og:title" content="{html.escape(full_title, quote=True)}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
{alternates}
<link rel="icon" href="{pre}assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{pre}assets/css/style.css">
</head>
<body class="page-{nav_key}">
<a class="skip-link" href="#main">{ui['skip']}</a>
<header class="site-header">
  <div class="container header-inner">
    <a class="brand" href="index.html" aria-label="Michel Mordant — home">
      <span class="brand-mark" aria-hidden="true">MM</span>
      <span class="brand-text"><span class="brand-name">Michel Mordant</span><span class="brand-sub">Percussion World</span></span>
    </a>
    <nav id="site-nav" class="site-nav" aria-label="{ui['nav_label']}">
      <ul>
{nav_items}
      </ul>
      <div class="nav-lang">
        <p>{ui['language']}</p>
        <ul>{lang_links}</ul>
      </div>
    </nav>
    <div class="header-tools">
      <div class="lang">
        <button class="lang-toggle" type="button" aria-expanded="false" aria-controls="lang-menu" aria-label="{ui['choose_language']}">
          <svg viewBox="0 0 24 24" width="17" height="17" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.6 2.8 3.9 5.8 3.9 9s-1.3 6.2-3.9 9c-2.6-2.8-3.9-5.8-3.9-9S9.4 5.8 12 3z"/></svg>
          <span>{lang.upper()}</span>
          <svg class="chev" viewBox="0 0 10 6" width="9" height="6" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M1 1l4 4 4-4"/></svg>
        </button>
        <ul id="lang-menu" class="lang-menu">{lang_links}</ul>
      </div>
      <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav"><span class="nav-toggle-bars" aria-hidden="true"></span><span class="nav-toggle-label">{ui['menu']}</span></button>
    </div>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="site-footer">
  <div class="container footer-grid">
    <div class="footer-about">
      <p class="footer-brand">Michel Mordant</p>
      <p>{ui['footer_about']}</p>
      <p><a class="footer-mail" href="mailto:{EMAIL}">{EMAIL}</a></p>
    </div>
    <div>
      <p class="footer-head">{ui['explore']}</p>
      <ul>{explore}
<li><a href="links.html">{ui['links']}</a></li></ul>
    </div>
    <div>
      <p class="footer-head">{ui['connect']}</p>
      <ul>{social}</ul>
      <ul class="footer-lang">{lang_links}</ul>
    </div>
  </div>
  <div class="container footer-base">
    <p>{ui['footer_rights']}</p>
    <p class="footer-credit">{ui['webcredit']} <a href="mailto:{WEBMASTER_EMAIL}">{WEBMASTER}</a> &middot; <a href="copyright.html">{ui['copyright']}</a></p>
  </div>
</footer>
<div class="lightbox" hidden>
  <figure class="lightbox-figure">
    <img alt="">
    <figcaption></figcaption>
  </figure>
  <button class="lightbox-close" type="button" aria-label="{ui['close']}">&times;</button>
  <button class="lightbox-prev" type="button" aria-label="{ui['prev']}">&#8249;</button>
  <button class="lightbox-next" type="button" aria-label="{ui['next']}">&#8250;</button>
</div>
<script src="{pre}assets/js/site.js" defer></script>
</body>
</html>
"""


def redirect_page(target):
    return f"""<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="robots" content="noindex">
<title>Michel Mordant — Percussion World</title>
<link rel="canonical" href="{DOMAIN}/{target}">
<meta http-equiv="refresh" content="0; url={target}">
</head>
<body>
<p>Deze pagina is verhuisd / This page has moved: <a href="{target}">{target}</a></p>
</body>
</html>
"""


# ---------------------------------------------------------------- main
def read_page(p):
    text = p.read_text(encoding="utf-8")
    head = text.split("\n\n", 1)[0]
    meta = dict(re.findall(r"<!--\s*(\w+):\s*(.*?)\s*-->", head))
    body = re.sub(r"^(\s*<!--.*?-->\s*)+", "", text, count=1, flags=re.S)
    body = re.sub(r"\{\{m:(.*?)\}\}", lambda m: html.escape(media_url(m.group(1)), quote=True), body)
    return meta, body


def page_strings(meta, soup):
    """Alle vertaalbare teksten van een pagina, in volgorde."""
    out = [meta["title"], meta["description"]]
    for t in soup.find_all(True):
        for a in ATTRS:
            if t.get(a):
                out.append(norm(t[a]))
    out += [src for _, src, _ in segments_of(soup)]
    return [s for s in out if has_letters(s)]


def extract(pages):
    SEGDIR.mkdir(parents=True, exist_ok=True)
    seen = set()
    per_page = {}
    for f in sorted(SEGDIR.glob("*.txt")):
        rows = [l.split("\t", 1) for l in f.read_text(encoding="utf-8").splitlines() if "\t" in l]
        per_page[f.stem] = rows
        seen.update(src for _, src in rows)
    added = 0
    for p in pages:
        meta, body = read_page(p)
        rows = per_page.setdefault(p.stem, [])
        nxt = max((int(n) for n, _ in rows), default=0) + 1
        for s in page_strings(meta, BeautifulSoup(body, "html.parser")):
            if s not in seen:
                seen.add(s)
                rows.append([str(nxt), s])
                nxt += 1
                added += 1
        (SEGDIR / f"{p.stem}.txt").write_text("".join(f"{n}\t{s}\n" for n, s in rows), encoding="utf-8")
    print(f"extract: {added} nieuwe segmenten, {len(seen)} totaal")


def main():
    pages = sorted(SRC.glob("*.html"))
    if EXTRACT:
        extract(pages)
        return
    cat = load_catalogue()
    for lang in LANGS:
        out_dir = SITE if lang == "nl" else SITE / lang
        out_dir.mkdir(parents=True, exist_ok=True)
        pre = "" if lang == "nl" else "../"
        for p in pages:
            meta, body = read_page(p)
            page_lang = meta.get("lang", "en")
            soup = BeautifulSoup(body, "html.parser")
            tr = lambda s: translate(s, lang, page_lang, cat, p.stem)  # noqa: E731
            for t in soup.find_all(True):
                for a in ATTRS:
                    if t.get(a) and has_letters(t[a]):
                        t[a] = re.sub(r"</?\d+/?>", "", tr(norm(t[a])))
                for a in ("src", "href"):
                    if t.get(a, "").startswith(("media/", "assets/")):
                        t[a] = pre + t[a]
            for el, src, tags in segments_of(soup):
                if not has_letters(src):
                    continue
                literal = bool(set(el.get("class", [])) & LITERAL) or el.name == "cite" or el.find_parent(["cite"]) is not None or el.find_parent(class_=["pill-list", "link-columns"]) is not None
                new = translate(src, lang, page_lang, cat, p.stem, tags, literal)
                if new != src:
                    el.clear()
                    el.append(BeautifulSoup(decode(new, tags), "html.parser"))
            meta = dict(meta, title=tr(meta["title"]), description=tr(meta["description"]))
            (out_dir / p.name).write_text(render(lang, p.name, meta, str(soup)), encoding="utf-8")
    for old, new in REDIRECTS.items():
        (SITE / old).write_text(redirect_page(new), encoding="utf-8")
    print(f"gebouwd: {len(pages)} pagina's x {len(LANGS)} talen, {len(media_map)} mediabestanden, {len(REDIRECTS)} doorverwijzingen")
    for lang in ("nl", "de"):
        rows = sorted(set(untranslated[lang]))
        (I18N / f"_onvertaald-{lang}.txt").write_text("".join(f"{pg}\t{s}\n" for pg, s in rows), encoding="utf-8")
        print(f"  nog te controleren ({lang}): {len(rows)}")
    rows = sorted(set(untranslated["en"]))
    if rows:
        print(f"  nog te controleren (en): {len(rows)}")
        (I18N / "_onvertaald-en.txt").write_text("".join(f"{pg}\t{s}\n" for pg, s in rows), encoding="utf-8")
    if missing:
        print("ONTBREKENDE MEDIA:")
        for m in sorted(set(missing)):
            print("  ", m)
        sys.exit(1)


if __name__ == "__main__":
    main()
