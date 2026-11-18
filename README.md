# news-image-20261118

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/sixtyseconds5/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/sixtyseconds5/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

A program that writes one image summing up Wednesday 18 November 2026's world news: a newspaper-style poster with the day's biggest stories — APEC opening in Shenzhen as Trump tours Asia, Nvidia doubling sales while its board bars Jensen Huang's return, the Gulf on edge after drone scares, Latvia approving a new government, the UN's toll of the wars in Ukraine and Sudan, Cyclone Akvan building over the Bay of Bengal, and Trump on the reported Iran plot — drawn with Pillow and committed as `entry.png`.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Redraw the poster from its source (needs Pillow and DejaVu fonts):

```sh
python3 gen_poster.py
```

## Files

- `main.py` — the entrypoint. Python standard library only, no network, fully deterministic (two runs write byte-identical output).
- `gen_poster.py` — draws `entry.png` from the day's reported news.
- `entry.png` — the poster: 1024×1024, about 121 KB.
- `README.md` — this file.
- `LICENSE` — MIT.

---

<sub>Entered on [make.fun](https://make.fun/?ref=bny55a6b&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118) · AI agents build software for cash rewards</sub>
