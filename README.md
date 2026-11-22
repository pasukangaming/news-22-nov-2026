# 22 November 2026 in One Image

A newspaper-style front page summing up Sunday 22 November 2026's world
news, drawn from scratch with PIL.

Lead story: **COP31 collapsed** — the climate summit in Antalya ended with
no deal after the EU rejected a text with no mention of fossil fuels.

Also covered: Iran strikes US bases in Bahrain; 'El Chapo Isidro' captured
in Sinaloa; a Russian missile hits Kryvyi Rih; US stocks slide into
correction; the World Court rules Myanmar committed genocide against the
Rohingya; the EU and Indonesia sign a landmark trade deal.

## How it is built

`main.py` (standard library only) calls `draw_image.py`, which draws the
1024x1024 PNG deterministically with PIL and writes it to
`$MAKEFUN_OUTPUT_DIR/entry.png` (default `out/`). Running it twice
produces byte-identical output.

## Entry

make.fun bounty **news-image-20261122** — "Sum up 22 November's world
news in one image". Built for @arif-teguh-ristyan.
