"""Entry point: draw the 22 November 2026 world-news image.

Writes entry.png into MAKEFUN_OUTPUT_DIR (default "out"). The drawing is
fully deterministic, so repeated runs produce byte-identical output.
"""

import os
from pathlib import Path

import draw_image


def main():
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "out"))
    out_dir.mkdir(parents=True, exist_ok=True)
    draw_image.render(out_dir / "entry.png")


if __name__ == "__main__":
    main()
