"""Toont per pagina de segmenten die nog geen eigen vertaling hebben en die de woordenlijst niet (volledig) dekt."""
import re, sys
sys.argv, pages = sys.argv[:1], sys.argv[1:]
import build
cat = build.load_catalogue()
EN = re.compile(r"\b(the|and|with|of|for|from|by|was|were|is|are|his|this|that|their|has|have|into|also|which|who|at|on|to|in|a|an|as|all|new|first|more|other|after|before|since|until|started|stopped|teaching|taught|see|here)\b")
for pg in pages:
    lang = dict(re.findall(r"<!--\s*(\w+):\s*(.*?)\s*-->", (build.SRC / f"{pg}.html").read_text().split("\n\n", 1)[0])).get("lang", "en")
    for line in (build.SEGDIR / f"{pg}.txt").read_text().splitlines():
        n, src = line.split("\t", 1)
        e = cat.get(src, {})
        need = [l for l in build.LANGS if l != lang and l not in e]
        if not need:
            continue
        if lang == "en":
            out = re.sub(r"<(\d+)>[^<]*</\1>", "", build.glossary(src, "nl"))
            plain = re.sub(r"<[^>]+>", " ", out)
            if not EN.search(plain) and build.glossary(src, "nl") != src:
                continue
            if not EN.search(plain) and len(plain.split()) > 3:
                continue  # namen, titels
        print(f"{pg}:{n}\t{src[:600]}")
