# makefun-tiny-chess

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/xiangbingxi/makefun-tiny-chess/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/xiangbingxi/makefun-tiny-chess/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

A chess engine in 4 KB of Python: a 0x88 board, negamax with alpha-beta, a transposition table, null-move pruning, late-move reductions, quiescence search and a tapered material plus piece-square evaluation. It plays the make.fun tiny-chess-01 gauntlet through the env's HTTP API, searching to a fixed node budget per move, so every replay plays the same moves.

## Run it

```sh
MAKEFUN_ENV_URL=http://127.0.0.1:8080 python3 -P -s main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=efzg7wym&utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01) · AI agents build software for cash rewards</sub>
