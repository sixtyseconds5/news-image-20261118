"""News-image entry: copy the poster to the grader's output directory.

The image (entry.png, drawn locally from real 18 November 2026 news with
gen_poster.py) sits beside this file. The grader runs with no network, so
this program only copies bytes: it is deterministic and stdlib-only.
"""
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))

SRC = HERE / "entry.png"
if not SRC.is_file():
    raise SystemExit(f"missing poster image: {SRC}")

OUT.mkdir(parents=True, exist_ok=True)
shutil.copyfile(SRC, OUT / "entry.png")
