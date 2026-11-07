#!/usr/bin/env python3
"""Search the local Ellen G. White library (public-domain English editions).

Commands:
  list                                  show all books (code, title, year, source type)
  search QUERY [--book CODE ...] [--any] [--phrase] [--regex] [--limit N] [--context] [--include-index]
  page CODE PAGE                        print one printed page of a book (for exact quoting)
  para CODE PAGE                        print the paragraphs that touch that page, unbroken
  doc "Lt 5, 1849"                      print a whole letter or manuscript (letters & manuscripts volumes)
  search ... --lang uk                  only books in that language (en = English originals, uk = Ukrainian translations)

QUERY by default matches paragraphs containing ALL words (case-insensitive,
punctuation and OCR spacing ignored). --any = at least one word. --phrase = the
exact word sequence. --regex = Python regex on normalized text.
Index / table-of-contents lines are skipped unless --include-index is given.
Each hit prints: book code, edition, page(s), a link to the scan/source page, and the paragraph.
"""
import gzip, json, os, re, sys, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
LIB = os.path.normpath(os.path.join(HERE, "..", "library"))
MARK = re.compile(r"\{p\. ([^}]+)\}")

def catalog():
    return json.load(open(os.path.join(LIB, "catalog.json"), encoding="utf-8"))

def norm(s):
    s = MARK.sub(" ", s)
    s = unicodedata.normalize("NFKD", s)
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = re.sub(r"[^\w']+", " ", s.lower())
    return re.sub(r"\s+", " ", s).strip()

_RAW = {}
def raw_text(b):
    if b["code"] not in _RAW:
        path = os.path.join(LIB, b["file"])
        _RAW[b["code"]] = (gzip.open(path, "rt", encoding="utf-8") if path.endswith(".gz") else open(path, encoding="utf-8")).read()
    return _RAW[b["code"]]

def may_contain(b, words):
    """Cheap pre-check before splitting a whole book into paragraphs."""
    low = norm(raw_text(b)) if len(raw_text(b)) < 200000 else unicodedata.normalize("NFKD", raw_text(b).lower()).replace("’", "'")
    return all(w.split("'")[0] in low for w in words)

def load_book(b):
    text = raw_text(b)
    body = text.split("\n---\n", 1)[1] if text.startswith("---\n") else text
    paras, page, art, sub = [], None, None, None
    for blk in re.split(r"\n\s*\n", body):
        blk = blk.strip()
        if not blk: continue
        if blk.startswith("## "): art, sub = blk[3:].strip(), None; continue
        if blk.startswith("### "): sub = blk[4:].strip()
        ms = MARK.findall(blk)
        lead = MARK.match(blk)
        if lead: page = lead.group(1)
        start = page
        if ms: page = ms[-1]
        clean = MARK.sub(lambda m: f"[p. {m.group(1)}]", blk)
        clean = re.sub(r"^\[p\. [^\]]+\]\s*", "", clean)
        if not clean: continue
        pages = [start] + [p for p in ms if p != start] if start else ms
        paras.append({"pages": [p for p in pages if p], "text": clean, "art": art, "sub": sub})
    return paras

def looks_like_index(text):
    toks = text.split()
    if len(toks) < 6: return False
    nums = sum(1 for t in toks if re.fullmatch(r"[\d,;.\-–]+", t))
    return nums / len(toks) > 0.2 or text.count("....") > 2

def link(b, page):
    pm = b.get("_pagemap")
    if pm is None and b.get("pagemap"):
        pp = os.path.join(LIB, b["pagemap"])
        pm = json.load(gzip.open(pp, "rt", encoding="utf-8") if pp.endswith(".gz") else open(pp, encoding="utf-8"))["pages"]
        b["_pagemap"] = pm
    if b["source"] == "archive.org" and pm and page in pm:
        v = pm[page]
        item, leaf = (v.rsplit(":", 1)[0], int(v.rsplit(":", 1)[1])) if isinstance(v, str) else (b["item"], v)
        return f"https://archive.org/details/{item}/page/n{leaf-1}/mode/1up"
    if b["source"] == "gutenberg" and b.get("anchor") and page and page.isdigit():
        return b["url_html"] + "#" + b["anchor"].format(n=int(page))
    return b.get("url")

def art_note(p):
    s = f"Article: \"{p['art']}\""
    if p.get("sub"):
        s += (f"\nCAUTION: this paragraph comes after the heading \"{p['sub']}\" inside the extracted text. It may be her subheading, "
              "or an unsigned item by someone else that follows her article. Read the article with `page` and quote it as hers only if it clearly continues her article.")
    return s

def fmt_pages(ps):
    ps = [p for p in ps if p]
    if not ps: return "p. ?"
    if re.match(r"(Lt|Ms) ", ps[0]): return ps[0] if len(ps) == 1 else f"{ps[0]} – {ps[-1]}"
    return f"p. {ps[0]}" if len(ps) == 1 else f"pp. {ps[0]}–{ps[-1]}"

def cite(b, ps):
    return f"{b['code']} — {b['title']} ({b['year']}), {fmt_pages(ps)}"

def main(argv):
    if not argv or argv[0] in ("-h", "--help"): print(__doc__); return
    cat = catalog(); books = {b["code"]: b for b in cat["books"]}
    cmd = argv[0]
    if cmd == "list":
        for b in cat["books"]:
            print(f"{b['code']:7} {b.get('lang','en'):3} {b['year']:<14} {b['quality']:10} {b['title']}")
        return
    if cmd == "doc":
        did = re.sub(r"\s+", " ", " ".join(argv[1:])).strip().rstrip(",")
        found = False
        for b in cat["books"]:
            if b.get("kind") != "letters": continue
            hits = [p for p in load_book(b) if p["pages"] and p["pages"][0].startswith(did + ", par.")]
            if not hits: continue
            found = True
            print(f"## {did} — in {b['code']}: {b['title']}\nSource: {link(b, hits[0]['pages'][0])}\nText quality: {b['quality']}")
            if hits[0].get("art"): print(f"Header: {hits[0]['art']}")
            print()
            for p in hits: print(f"[{p['pages'][0]}] " + p["text"] + "\n")
        if not found: sys.exit(f"Document {did} not found. Write it like: Lt 5, 1849  or  Ms 12, 1888")
        return
    if cmd in ("page", "para"):
        code, pg = argv[1], argv[2]
        b = books.get(code) or sys.exit(f"Unknown book code {code}. Use: list")
        hits = [p for p in load_book(b) if pg in p["pages"]]
        if not hits: sys.exit(f"Page {pg} not found in {code}.")
        print(f"## {cite(b, [pg])}\nSource: {link(b, pg)}\nText quality: {b['quality']}\n")
        last_art = None
        for p in hits:
            if b.get("kind") == "periodical" and p["art"] != last_art:
                print(f"=== Article: \"{p['art']}\" ==="); last_art = p["art"]
            pre = f"[p. {p['pages'][0]}] " if p["pages"] and p["pages"][0] != pg else ""
            print(pre + p["text"] + "\n")
        return
    if cmd == "search":
        args, opts = [], {"book": [], "limit": 25}
        i = 1
        while i < len(argv):
            a = argv[i]
            if a == "--book": opts["book"].append(argv[i+1]); i += 2; continue
            if a == "--limit": opts["limit"] = int(argv[i+1]); i += 2; continue
            if a == "--lang": opts["lang"] = argv[i+1]; i += 2; continue
            if a in ("--any", "--phrase", "--regex", "--context", "--include-index"): opts[a[2:]] = True; i += 1; continue
            args.append(a); i += 1
        q = " ".join(args)
        nq = norm(q); words = nq.split()
        sel = [books[c] for c in opts["book"]] if opts["book"] else cat["books"]
        if opts.get("lang"): sel = [b for b in sel if b.get("lang", "en") == opts["lang"]]
        n = 0
        for b in sel:
            if not opts.get("regex") and words and not may_contain(b, words): continue
            paras = load_book(b)
            for k, p in enumerate(paras):
                t = norm(p["text"])
                if opts.get("regex"): ok = re.search(q, t) is not None
                elif opts.get("phrase"): ok = (" " + nq + " ") in (" " + t + " ")
                elif opts.get("any"): ok = any(re.search(r"\b" + re.escape(w) + r"\b", t) for w in words)
                else: ok = all(re.search(r"\b" + re.escape(w) + r"\b", t) for w in words)
                if not ok: continue
                if not opts.get("include-index") and looks_like_index(p["text"]): continue
                n += 1
                if n > opts["limit"]: continue
                print(f"### {n}. {cite(b, p['pages'])}  [{b['quality']}]")
                print(f"Source: {link(b, p['pages'][0] if p['pages'] else None)}")
                if b.get("kind") == "periodical": print(art_note(p))
                if b.get("kind") == "letters" and p.get("art"): print(f"Document header: {p['art']}")
                if b.get("translation_of"): print(f"Ukrainian translation of {b['translation_of']} ({b['year']}); quote it as the published translation, the English original stays primary.")
                if opts.get("context") and k > 0: print("(prev) " + paras[k-1]["text"][-300:])
                print(p["text"])
                if opts.get("context") and k + 1 < len(paras): print("(next) " + paras[k+1]["text"][:300])
                print()
        if n > opts["limit"]:
            print(f"[shown {opts['limit']} of {n} matching paragraphs — narrow the query, use --book, or raise --limit]")
        elif n: print(f"[{n} matching paragraphs]")
        if n == 0: print("NO MATCHES. Try other words, --any, or a different spelling (OCR texts may contain errors).")
        return
    print(__doc__)

if __name__ == "__main__":
    main(sys.argv[1:])
