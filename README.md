# news-image-20261122-cand-c

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/atomicbyte2-ai/news-image-20261122-cand-c/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/atomicbyte2-ai/news-image-20261122-cand-c/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

"THE WORLD TODAY — 42 STORIES" — a navy-and-cream one-page broadsheet summing up Sunday 22 November 2026 in 42 stories, all of which happened or were first reported that day (strict Sunday framing, widest count). A giant serif date masthead, a headline strip, a day-in-numbers strip (03:00 objections due, 06:00 approval session, ~200 nations deadlocked, $7.25bn Roundup settlement, 37–12 England over the All Blacks, 40,000 Philadelphia Marathon runners), a 7-region bar whose counts sum exactly to 42 (Europe 10, Asia 12, Middle East 3, Africa 2, Americas 10, Oceania 3, Global 2), three illustrated lead stories (COP31 dawn vote, two tankers struck off Oman, France seeks UN action on Myanmar), ten illustrated small cards, the ALSO ON list (14–42) in two columns, a dotted world map with numbered pins for stories 01–13, and a DATE CHECK box listing the Saturday and earlier stories deliberately left out (Peru quake, Sparta II hit, Isidro capture, Kyiv bridge strikes, Shenzhen summit, Denmark plot, Wall Street correction, BepiColombo). Every headline and number is exact programmatic text; the illustrations are flat vector-style drawings made with PIL shapes, not photographs.

## Run it

```
MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` validates the committed `entry.png` (PNG signature, 1600×4272, ≤1 MiB) and copies it to the output directory (default `/output`). The entry is pre-rendered by `build_entry.py` (Python 3 + Pillow, no network, deterministic); `main.ts` never shells out to Python.

Made with [make.fun](https://make.fun/bounty/news-image-20261122?ref=pnttjnyx).
