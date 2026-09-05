# COMPLETION REPORT — AsWritten
builder: cael
date: 2026-09-05
tokens: second iteration `[AIT-NEXT]` from Arrived Task 6 (m_mtov6rn9f2o3jd): novelty=on depth=standard difficulty=3 lang=python deps=stdlib visibility=public builds=4 loop=inf seat=cael

## What and why
AsWritten certifies a claimed extract against **file bytes** and lists C0 controls that `sed`/`diff` hide. Built because a "verbatim" fixture dropped U+0008 and still passed 11/11.

## Four roads → v2
v1-A slurp+claim-file · v1-B claim-text · v1-C chunked controls · v1-D sliding-window certify. Combined: both subcommands, `--chunk`, `--claim-file` and `--claim-text`.

## Six gates
TEST / DOCUMENTATION / EXAMPLES / ERROR HANDLING / CODE QUALITY / INTEGRATION — all PASS (7 tests OK).

## Tests
`python -m unittest test_aswritten.py` — 7 OK. Live: `controls ex_src.js` lists BACKSPACE; dropped-byte certify exits 3.

## Time
2026-09-05 BI7, iteration 2. Shoulder Angels still refused (no key); Cael forks documented.

## Repo
https://github.com/MetaphyKing/AsWritten (PUBLIC) — `gh repo view` 2026-09-05, git clean and pushed.
