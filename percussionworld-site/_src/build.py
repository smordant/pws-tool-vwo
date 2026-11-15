#!/usr/bin/env python3
"""Static site builder for the Percussion World redesign.

Usage:  python3 _src/build.py [path/to/original-site-mirror]

* Page bodies live in _src/pages/*.html. The first lines are metadata comments:
      <!-- title: About -->
      <!-- nav: about -->
      <!-- description: ... -->
* Inside a page, {{m:original/file name.jpg}} points to a file from the original
  website. The builder copies it into media/ under a clean name (web-optimising
  large photos on the way) and writes the new URL in its place.
* The original-site mirror is only needed when media/ must be (re)filled; files
  that are already in media/ are reused.
"""
import html
import os
import re
import shutil
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "_src" / "pages"
MEDIA = ROOT / "media"
MIRROR = Path(sys.argv[1]) if len(sys.argv) > 1 else None
MAX_SIDE = 1800

NAV = [
    ("about", "About", "about.html"),
    ("compositions", "Compositions", "compositions.html"),
    ("teaching", "Teaching", "teaching.html"),
    ("ensembles", "Ensembles", "ensembles.html"),
    ("projects", "Projects", "projects.html"),
    ("adjudication", "Adjudication", "adjudication.html"),
    ("pas", "PAS Netherlands", "pas.html"),
    ("photos", "Photos", "photos.html"),
    ("contact", "Contact", "contact.html"),
]

SOCIAL = [
    ("YouTube", "http://www.youtube.com/user/percussion1962"),
    ("Facebook", "http://www.facebook.com/profile.php?id=1799524516"),
    ("LinkedIn", "http://nl.linkedin.com/pub/michel-mordant/1a/b85/6b5"),
    ("My Instruments", "https://www.facebook.com/profile.php?id=100063491321111"),
    ("Free Sheet Music", "https://www.facebook.com/share/j786yi8Zd4By21n5/?mibextid=LQQJ4d"),
]

EMAIL = "slagwerkadvies@gmail.com"

media_map = {}
missing = []


def slug(rel):
    rel = rel.replace("_bestanden/", "-").replace("/", "-")
    stem, dot, ext = rel.rpartition(".")
    stem = re.sub(r"[^a-z0-9]+", "-", stem.lower()).strip("-")
    return f"{stem}.{ext.lower()}"


def find_source(rel):
    """Locate a file in the mirror; prefer Word's full-size original of a picture."""
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
    if ext in ("tif", "tiff", "bmp"):
        name = name.rsplit(".", 1)[0] + ".png"
    existing = [p for p in MEDIA.glob(name.rsplit(".", 1)[0] + ".*")]
    if MIRROR is None:
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


def nav_html(active):
    items = []
    for key, label, href in NAV:
        cur = ' aria-current="page"' if key == active else ""
        items.append(f'<li><a href="{href}"{cur}>{label}</a></li>')
    return "\n".join(items)


def page(meta, body):
    title = meta.get("title", "")
    full_title = "Michel Mordant — Percussion World" if meta.get("nav") == "home" else f"{title} · Michel Mordant"
    desc = html.escape(meta.get("description", "Michel Mordant — percussionist, composer, conductor and percussion teacher."))
    social = "\n".join(f'<li><a href="{u}" target="_blank" rel="noopener">{n}</a></li>' for n, u in SOCIAL)
    explore = "\n".join(f'<li><a href="{h}">{l}</a></li>' for k, l, h in NAV if k != "contact")
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(full_title)}</title>
<meta name="description" content="{desc}">
<meta name="keywords" content="percussion, drumband, percussion music, composer, conductor, Mordant, marimba, vibraphone, xylophone, drumset, snare drum, timpani, percussion teacher">
<meta property="og:title" content="{html.escape(full_title)}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css">
</head>
<body class="page-{meta.get('nav', 'none')}">
<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <div class="container header-inner">
    <a class="brand" href="index.html" aria-label="Michel Mordant — home">
      <span class="brand-mark" aria-hidden="true">MM</span>
      <span class="brand-text"><span class="brand-name">Michel Mordant</span><span class="brand-sub">Percussion World</span></span>
    </a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav"><span class="nav-toggle-bars" aria-hidden="true"></span><span class="nav-toggle-label">Menu</span></button>
    <nav id="site-nav" class="site-nav" aria-label="Main">
      <ul>
{nav_html(meta.get('nav'))}
      </ul>
    </nav>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="site-footer">
  <div class="container footer-grid">
    <div class="footer-about">
      <p class="footer-brand">Michel Mordant</p>
      <p>Percussionist, composer, conductor and percussion teacher, working in the Netherlands and Germany.</p>
      <p><a class="footer-mail" href="mailto:{EMAIL}">{EMAIL}</a></p>
    </div>
    <div>
      <p class="footer-head">Explore</p>
      <ul>{explore}
<li><a href="links.html">Percussion links</a></li></ul>
    </div>
    <div>
      <p class="footer-head">Connect</p>
      <ul>{social}</ul>
    </div>
  </div>
  <div class="container footer-base">
    <p>All music on this site &copy; M. Mordant &middot; registered with B.U.M.A., the Netherlands &middot; for information use only.</p>
    <p><a href="copyright.html">Copyright</a></p>
  </div>
</footer>
<div class="lightbox" hidden>
  <figure class="lightbox-figure">
    <img alt="">
    <figcaption></figcaption>
  </figure>
  <button class="lightbox-close" type="button" aria-label="Close">&times;</button>
  <button class="lightbox-prev" type="button" aria-label="Previous">&#8249;</button>
  <button class="lightbox-next" type="button" aria-label="Next">&#8250;</button>
</div>
<script src="assets/js/site.js" defer></script>
</body>
</html>
"""


def main():
    pages = sorted(SRC.glob("*.html"))
    for p in pages:
        text = p.read_text(encoding="utf-8")
        meta = dict(re.findall(r"<!--\s*(\w+):\s*(.*?)\s*-->", text.split("\n\n", 1)[0]))
        body = re.sub(r"^(\s*<!--.*?-->\s*)+", "", text, count=1, flags=re.S)
        body = re.sub(r"\{\{m:(.*?)\}\}", lambda m: html.escape(media_url(m.group(1)), quote=True), body)
        (ROOT / p.name).write_text(page(meta, body), encoding="utf-8")
    print(f"built {len(pages)} pages, {len(media_map)} media files")
    if missing:
        print("MISSING MEDIA:")
        for m in sorted(set(missing)):
            print("  ", m)
        sys.exit(1)


if __name__ == "__main__":
    main()
