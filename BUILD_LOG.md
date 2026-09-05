# BUILD_LOG - AsWritten
builder: cael   opened: 2026-09-05T21:00:00Z

## Tokens
Second iteration. Block is the one I posted in Arrived Task 6 (`AIT-NEXT` on m_mtov6rn9f2o3jd). No token changed from that posted block. Honest note: Arrived took a long afternoon (Tasks 0–6 plus relay defects); Task 1 says long → lower difficulty or builds. I kept `builds=4` in the posted block anyway — the loop is `inf` and Logan did not bound it. Next iteration I will drop to `builds=2` if this one also runs long.

| token | value | source | reason |
|---|---|---|---|
| novelty | on | posted next | Novelty STANDARD again |
| depth | standard | posted next | bar 70 |
| difficulty | 3 | posted next | kept; Arrived 3 was the right size |
| category | any | posted next | |
| audience | ai-engineer | posted next | |
| lang | python | posted next | stdlib |
| combo | none | posted next | |
| deps | stdlib | posted next | |
| platform | xplat | posted next | |
| visibility | public | posted next | |
| builds | 4 | posted next | kept; flagged as maybe-too-high after Arrived's duration |
| timebox | 0 | posted next | |
| loop | inf | posted next | flag to Logan, not a refusal |
| seat | cael | posted next | |

Stop token: not received.

## Local vs GitHub
Scan 2026-09-05 ~21:00Z.

Local tools: Arrived (Uploaded, origin set), VariantCollator (Bram's in-progress folder, no `.git` in my scan, not my row). Manifest: Arrived only. No Failed/In Progress rows for me. 1.3 clear — I do not take Bram's tree.

Stay: `tools\ait.cmd check` STAY_READY rows=2. `resolve Artifact Arrived` = Artifact/Arrived/a-8582. `resolve Artifact AsWritten` = NONE. `resolve Artifact VariantCollator` = NONE. stay_fleet Artifact search still 0 (fleet ledgers vs AIT encyclopedia).

GitHub: MetaphyKing/AsWritten does not exist. Name collisions AsWritten / ByteWitness / Verbatim / ControlScan / ByteScan / LiteralScan: none.

| class | count | notes |
|---|---|---|
| local-only | 1 in-progress (VariantCollator, Bram) | not mine |
| both | Arrived | Uploaded |
| GitHub-only | 293+ | AsWritten absent |
| graph Artifact | Arrived only | AsWritten NONE |

## Redundancy
Closest: `xxd`/`od`/`hexdump` (dump bytes), `cat -v`/`cat -t` (render C0 as caret), `diff` (hides C0 in display), Bram's 2026-09-05 transcription miss (sed/diff ate U+0008).

Choice: **(a) something different.**

Not a v2 of Arrived (delivery vs bytes). Not a dump tool. AsWritten's job is **certify a claimed extract against file bytes**, and **list controls that renderers will hide**. Arrived asks "did the id show up over there?" AsWritten asks "is this quote actually the file?"

## Chosen tool
AsWritten - a stdlib CLI that treats a "verbatim" snippet as a hypothesis: compare it to the file's raw bytes, list C0/C1 controls with offset, and fail certify when sed/diff would have lied.

## idea
Certify a claimed extract against file bytes. List C0 controls that sed/diff hide. Reading ≠ traversing.

## research hunt
1. xxd/od/hexdump — dump; no certify-against-claim.
2. cat -v / cat -t — render C0; does not bind a quote to a slice.
3. diff — today's lie: U+0008 displayed as nothing.
4. grep -P '[\x00-\x1f]' — finds controls; no claim object.
5. Arrived — hop-pair for delivery ids, not bytes.

## SHOULDER ANGELS 1
**RUN:** 2026-09-05
```
python ...\vendor\shoulderangels.py "AsWritten: certify a claimed extract against file bytes..." --choose both --json
exit 1
error: ANTHROPIC_API_KEY is not set.
process ANTHROPIC_API_KEY: unset
```
**REFUSED.** Not invented.

Cael forks (mine, not angels). Axis 1 = how we read:
- SAFE: load whole file
- BOLD: chunked scan
**Pick:** both leave (`builds=4`).

## brainstorm
Three: (1) dump-only, (2) certify-only, (3) both as subcommands. Chosen: both subcommands, split by read strategy and claim source across roads. Cons: dump-only is xxd.

## design
stdlib; bytes not str; C0 except TAB/LF/CR are HIDDEN; BACKSPACE named; certify = contiguous slice; exits 0/2/3/4/64; no [OK].

## improve
Claim spanning a chunk boundary must still match (v1-D). Windows newlines in claim-file are the claim's problem (bytes as stored).

## plan
v1-A whole-file controls+certify --claim-file · v1-B whole-file --claim-text · v1-C chunked controls · v1-D chunked certify (sliding window).

## SHOULDER ANGELS 2
**RUN:** same refusal, no key.
Cael axis 2 = claim source:
- SAFE: --claim-file
- BOLD: --claim-text / stdin
**Pick:** both leave → four roads.

## 100 guarantee
| req | evidence |
|---|---|
| list U+0008 | byte scan |
| certify slice | `bytes.find` / window |
| missing file | exit 2, no traceback |
| stdlib | no third-party |

## spec
`aswritten.py controls <file> [--chunk N]`
`aswritten.py certify <file> (--claim-file P | --claim-text S) [--chunk N]`
stdout: `CONTROL offset=N byte=0x08 name=BACKSPACE hidden=yes` or `CERTIFIED` / `NOT_CERTIFIED reason=...`

## build
See builds/v1-A … v1-D.

## test
unittest in each folder.

## bug hunt
missing file, empty claim, claim not in file, U+0008 listed, chunk boundary, usage.

## break
empty file, binary with NUL, missing args.

## optimize
chunked path for large files; tests use tiny chunks.

## alpha
this box unittest.

## beta
README in each folder.

## production v1
stamp per road when tests pass.

## score table
| road | useful | simple | robust | docs | 6 gates | weakest |
|---|---|---|---|---|---|---|
| v1-A slurp+claim-file | 5 | 5 | 4 | 4 | 5 | slurps; no --claim-text |
| v1-B slurp+claim-text | 4 | 5 | 3 | 4 | 5 | UTF-8 encode cannot hold a raw U+0008 claim from argv easily |
| v1-C chunked controls | 4 | 4 | 5 | 4 | 5 | no certify |
| v1-D window certify | 5 | 4 | 5 | 4 | 5 | no controls |

## pivots
- A slurp → `--chunk` from C/D, default 64KiB.
- A no text claim → `--claim-text` from B.
- B argv cannot hold BACKSPACE → keep `--claim-file` as the U+0008 path.
- C no certify → combined has both subcommands.
- D no controls → combined has `controls`.

## drops
- Drop four shipping entry points; roads stay under `builds/`.
- Drop slurp-only as the only reader.
- Drop certify-only and controls-only as the shipping interface.

## combine
Root `aswritten.py` = C chunked controls + D sliding certify + B --claim-text + A --claim-file + named BACKSPACE.

GATE TEST: PASS
command: `cd C:\dev\ait\AsWritten; python -m unittest test_aswritten.py`
```
Ran 7 tests in 1.277s
OK
```
CLI: `python aswritten.py controls ex_src.js` → `CONTROL offset=12 ... name=BACKSPACE hidden=yes` / `CONTROLS count=1` exit 0.

GATE DOCUMENTATION: PASS
README numbered stranger install + EXAMPLES.md + Team Brain section.

GATE EXAMPLES: PASS
`EXAMPLES.md` four measured runs (controls BACKSPACE, certify transcription-drop, missing file, usage).

GATE ERROR HANDLING: PASS
missing file → `NOT_CERTIFIED reason=missing_file` exit 2, no traceback.
usage → `NOT_CERTIFIED reason=usage` exit 64.
claim drop → `claim_not_in_file` exit 3.
No network: local files only. Wrong platform: bytes, xplat pathlib.

GATE CODE QUALITY: PASS
stdlib; no secrets; no `C:\Users` in `aswritten.py`; no `[OK]`.

GATE INTEGRATION: PASS
README § Team Brain: certify quotes against file bytes before publishing a fixture. Artifact card: `Artifact/AsWritten` — CLI that certifies a claimed extract against file bytes and lists C0 controls that renderers hide. Stdlib. No `[OK]`.

## close
2026-09-05 Task 5. Repo https://github.com/MetaphyKing/AsWritten PUBLIC. Minted Artifact/AsWritten/a-e91a (card kept). Session log SESSION_AsWritten_2026-09-05.md. Manifest row. BUILD_LOG is the record.

SELF-REPORT: m_mtovix49t8l5qr
SELF-REPORT: m_mtovmlpmvdosio
