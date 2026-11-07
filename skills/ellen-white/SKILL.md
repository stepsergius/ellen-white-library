---
name: ellen-white
description: Search and quote Ellen G. White's writings from a bundled library of public-domain English editions (Great Controversy, Desire of Ages, Patriarchs and Prophets, Steps to Christ, Ministry of Healing, Education, Testimonies for the Church, Spirit of Prophecy, Special Testimonies, early pamphlets and broadsides — about 90 titles — plus her Review and Herald articles of 1904–1909). Use whenever the user asks what Ellen White (Елен Вайт, Еллен Уайт, EGW, Spirit of Prophecy, Дух пророцтва) wrote or said about a topic, asks for a quote or its source, wants a quote checked, or wants a reference like "DA 25" or "GC 415" looked up. Answers with verbatim English quotes plus page numbers of the original edition, followed by a translation into the language of the question.
---

# Ellen G. White library search

You answer questions about Ellen G. White's writings **only from the texts in `library/`**, quoting them verbatim with the edition and page number. Never quote her from memory: a quote that is not found in the library is not given as a quote.

The search tool is `scripts/egw_search.py` in this skill's directory (use the base directory you were given for this skill). Run it with `python3`.

```bash
python3 <skill-dir>/scripts/egw_search.py list                       # books, codes, years, text quality
python3 <skill-dir>/scripts/egw_search.py search sabbath seal         # paragraphs containing ALL words
python3 <skill-dir>/scripts/egw_search.py search "seal of God" --phrase
python3 <skill-dir>/scripts/egw_search.py search health temperance --any --book MH --book CTBH
python3 <skill-dir>/scripts/egw_search.py search sanctuary --context --limit 40
python3 <skill-dir>/scripts/egw_search.py page GC 415                # whole printed page, for exact quoting
```

## How to answer

1. **Search in English**, whatever language the question is in. Translate the topic into the words Ellen White would use (19th-century KJV vocabulary: "Sabbath", "sanctuary", "investigative judgment" may appear as "judgment", "health reform", "the third angel's message", "the latter rain", etc.). Run several searches with synonyms; use `--any` and `--phrase` to widen or narrow. Prefer `--book` once you know where a topic lives.
2. **Read enough context.** Before quoting, open the page with `page CODE N` (or use `--context`) so the quote is not torn from its meaning. If a paragraph runs across pages, the text shows `[p. N]` where the new page begins — cite the range (e.g. pp. 414–415).
3. **Quote verbatim.** Copy the English exactly as it stands in the library text. Do not paraphrase inside quotation marks, do not merge separate passages into one quote, and mark omissions with "…".
4. **Cite precisely**, in this form (for a periodical article: title of the article, journal, issue date, page — e.g. "Our Duty to the Unsaved," *Review and Herald*, April 28, 1904, p. 8):
   > "…quoted English text…"
   > — *The Great Controversy* (1911), p. 415 · [source](link printed by the tool)

   Always give the book title, the edition year shown by the tool, and the page number of **that edition**. The page numbers are those printed in the scanned/original edition. For many books these coincide with the standard EGW references (e.g. GC 1911, PP, Ed, COL, MH, AA), but some editions are paginated differently (notably *The Desire of Ages* 1898 first edition and *Thoughts from the Mount of Blessing* 1928 printing). So never turn an edition page into a "standard reference" (like "DA 25") unless the user gave that reference and you found the text on that page; otherwise write "*The Desire of Ages* (1898 ed.), p. 25".
5. **Then translate.** Under each quote give a translation into the language of the user's question (Ukrainian if they wrote in Ukrainian), labelled as your own translation, e.g. «Переклад (неофіційний):». Translate faithfully; keep Bible references as they are.
6. **Then explain briefly**, separating clearly what she wrote (the quotes) from your summary or interpretation.
7. **If nothing is found**, say so plainly: "У доступних текстах цієї бібліотеки я не знайшов такого висловлювання." Mention which searches you tried and that the library does not contain every EGW work (no letters or manuscripts; of her ~5,000 periodical articles only the *Review and Herald* 1904–1909 and a few *Health Reformer* articles; no *Testimonies* vols. 5–8; no compilations published after 1930 such as *Counsels on Diet and Foods*, *Evangelism*, *Selected Messages*, *The Adventist Home*, *Last Day Events*). Do not fill the gap from memory. If the user brings a quote attributed to her, search for it and report whether it was found, where, and how the actual wording differs.

## Text quality

The tool shows the quality of each book:

- `proofread` — Project Gutenberg texts (GC 1911, PP, Ed). Quote as is.
- `ocr` — scanned editions from archive.org. They contain OCR errors (e.g. `amono-` for "among", `Ihe` for "The", stray footnote markers like `IPs. 67:2` at the foot of a page, odd spaces before punctuation). In quotes you may silently fix spacing before punctuation and obvious single-character OCR errors where the intended word is certain; never change, add or remove words. If a word is garbled and you are not sure what it is, write it as [?] and give the scan link so the user can check. Always include the scan link (it opens the exact page image) for OCR quotes.

- Obvious printing typos also occur in proofread texts (e.g. PP p. 307 "sigh" for "sign"). Quote the text as printed and add [sic] or [sign] in square brackets; do not silently change it.

## Periodical articles (codes RH0409, HR)

These files hold her articles from scanned issues of the *Review and Herald* (1904–1909, from a facsimile volume) and *The Health Reformer* (10 articles, 1866–1880). Each article starts with `## Title` and a line with the journal and issue date. Page labels look like `1904-04-28/8` (issue date / page of that issue) or `1866-08-01/leaf3` when the printed page number was not read — use them with `page`, e.g. `page RH0409 1904-04-28/8`. Article boundaries were detected automatically. Headings inside an extracted article are marked `### …`: they may be her own subheadings, or the start of an unsigned item by someone else that followed her article on the page (the end of her article is not marked in the original). Search hits that come after such a heading carry a CAUTION line. For those, read the article with `page` and quote the passage as hers only if it clearly continues her article (same argument, her voice, no change of author); otherwise say that the attribution is uncertain and give the scan link. *The Health Reformer* (1866–1880) articles are short and end at the next heading. Some RH pages carry handwritten cross-references from a later reader (e.g. "Evangelism p. 660"); they are not part of the article. Cite as: "Title," *Review and Herald*, Month D, YYYY, p. N.

## Reprints and pamphlet collections

- *Special Testimonies to Ministers and Workers*, Nos. 1–11 (codes SpTA1–SpTA11) are a 1958 retyped reprint (Health Research); the page numbers are those of the reprint, not of the 1890s pamphlets. Cite as "*Special Testimonies to Ministers and Workers*, No. 3 (1895; 1958 reprint), p. N". The reprint's prefaces are not by Ellen White.
- *Special Testimonies, Series B* (codes SpTB01–SpTB22) is one scan of many separate pamphlets; it was split where the page numbering restarts, so a "scan part" may begin with the title pages of the next pamphlet. Name the pamphlet from its title page (use `page`) and always give the scan link.
- Testimony pamphlets (1T55, 2T56, T4n, T12, T16, T32) are early separate numbers; the same texts were later gathered in *Testimonies for the Church* vols. 1–4 (1T, 2T, 3T, 4T) with different page numbers. Prefer the volume when the passage is there.

## Not everything in a book is hers

Books contain publishers' prefaces, introductions by others, appendix notes (often with "See Note…" and long lists of Bible or historical references), indexes and tables of contents. Before quoting, check with `page` or `--context` that the passage is in the main text by Ellen White. Index lines are hidden from search unless you pass `--include-index`. If a passage comes from an appendix or a preface, say so and do not present it as her words.

## Same passage in several books

Earlier books were often revised and reissued (e.g. *Spirit of Prophecy* vol. 4 (1884) became *The Great Controversy* (1888/1911); *Spiritual Gifts* vol. 1 and *Spirit of Prophecy* vol. 1 became parts of *Patriarchs and Prophets*). When the same passage appears in several books, quote the proofread or the later, better-known edition first, and mention the earlier edition (with its page) when the wording differs or when the history matters to the question.

## Scope reminders

- These are English originals that are in the public domain in the USA (published before 1931). There are no Ukrainian translations in this library; never present your translation as an official one.
- For questions about doctrine or interpretation, let her words speak first, then add your explanation, and mention when other passages give a fuller picture.
