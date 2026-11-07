# Ellen G. White Library — Claude skill

A Claude Code plugin with one skill, **ellen-white**, that searches the writings of Ellen G. White and quotes them verbatim with the edition and page number, followed by a translation into the language of the question.

Плагін для Claude Code зі скілом **ellen-white**: шукає в текстах Елен Вайт, цитує дослівно англійською з точним виданням і сторінкою, а нижче дає переклад мовою запитання (наприклад, українською).

## Встановлення / Installation

У Claude Code (термінал або вкладка Code у застосунку Claude):

```
/plugin marketplace add stepsergius/ellen-white-library
/plugin install ellen-white@ellen-white-library
```

Потім просто питайте, наприклад: «Що Елен Вайт писала про суботу як печатку Бога?» або «Знайди джерело цитати: …».

Then ask, e.g.: "What did Ellen White write about the Sabbath as the seal of God?"

Python 3 is required (it is preinstalled on macOS and most Linux systems).

## What is inside

`skills/ellen-white/library/` holds the texts as Markdown, one file per book, with page markers `{p. N}` taken from the printed edition. `catalog.json` lists every book with its source. `scripts/egw_search.py` is the search tool the skill uses:

```
python3 skills/ellen-white/scripts/egw_search.py list
python3 skills/ellen-white/scripts/egw_search.py search "seal of God" --phrase
python3 skills/ellen-white/scripts/egw_search.py page GC 415
```

| Source | Quality |
|---|---|
| Project Gutenberg — *The Great Controversy* (1911), *Education* (1903), *Patriarchs and Prophets* (1913 printing) | proofread |
| Internet Archive scans — *The Desire of Ages* (1898), *Steps to Christ*, *The Ministry of Healing*, *The Acts of the Apostles*, *Christ's Object Lessons*, *Prophets and Kings*, *Early Writings*, *Gospel Workers*, *Life Sketches*, *Testimonies for the Church* vols. 1–4 and 9, *Spirit of Prophecy* vols. 1–4, *Spiritual Gifts*, *Special Testimonies* (Series A and B), early testimony pamphlets and broadsides (1846–1885), *Bible Sanctification*, *An Appeal to Mothers* and more | OCR (may contain recognition errors; every hit links to the page scan) |
| Scanned periodicals — her *Review and Herald* articles 1904–1909 (226 articles, from a facsimile volume) and a few *Health Reformer* articles (1866–1877) | OCR; article boundaries detected automatically |

Run `list` for the full list.

**Not included:** letters and manuscripts (the only complete digital edition comes from the Ellen G. White Estate, and part of it is under US copyright until 2047), most periodical articles (no public scans of the original issues were found apart from those above), *Testimonies* vols. 5–8 (no freely accessible scan), and compilations published after 1930 (*Counsels on Diet and Foods*, *Evangelism*, *Selected Messages*, *The Adventist Home*, *Last Day Events*, etc.), which are still under copyright.

## Page numbers

Page numbers are those of the edition in the library. For many books they match the standard EGW references (GC 1911, PP, Ed, COL, MH, AA …), but some editions differ — notably *The Desire of Ages* 1898 first edition. The skill therefore always cites the edition year with the page.

## Copyright

All texts are Ellen G. White's works published in the USA before 1931 and are in the public domain there. They come from Project Gutenberg (the Project Gutenberg License that accompanies those three texts is in `skills/ellen-white/library/PROJECT-GUTENBERG-LICENSE.txt`) and from public-domain scans on the Internet Archive. The texts are not from EGW Writings and are not affiliated with the Ellen G. White Estate. The scripts and skill instructions are released under the MIT License.
