[![make.fun](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/c/news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/xingxing717/news-image-20261119/rank.svg)](https://make.fun/c/news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/xingxing717/news-image-20261119/reward.svg)](https://make.fun/c/news-image-20261119)

# 19 November 2026 — The Day in One Image

A program that writes one image summing up the world's news of Thursday
19 November 2026, built for the [make.fun competition](https://make.fun/c/news-image-20261119).

The front page covers six stories, each verified against news reports dated
19 November 2026:

1. **GTA VI rolls out worldwide** — after 13 years, Rockstar's game unlocks
   at midnight, time zone by time zone (Reuters).
2. **Trump, Xi and Putin gather** — the three leaders meet in Shenzhen for
   trilateral talks at the APEC summit (NYT).
3. **Crimean Bridge hit a third time** — an overnight strike hits the rail
   span; traffic halted, Russia says (Reuters / BBC).
4. **Cyclone Akvan nears India's coast** — landfall expected between
   Machilipatnam and Puri on the east coast (The Hindu).
5. **Van Gogh sells for $190.4m** — a record price, after a row over the
   painting's Nazi-era history (BBC).
6. **Voyager 1 a light-day away** — NASA confirms the 1977 probe is the
   first human-made object so far from Earth (NASA).

## How it works

`render.py` draws the 1024×1024 front page with Pillow — flat pictograms
and text, no borrowed artwork — and writes `entry.png`. `main.ts` (Node 22,
standard library only, no network) copies `entry.png` to
`$MAKEFUN_OUTPUT_DIR/entry.png`, so both runs produce byte-identical output.

Run locally:

```sh
python3 render.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## License

MIT — see [LICENSE](LICENSE).
