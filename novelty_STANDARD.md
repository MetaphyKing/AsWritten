# AsWritten — Novelty Engine STANDARD score sheet
seat: cael   mode: STANDARD (bar 70)   date: 2026-09-05
iteration: 2 (after Arrived)

## 1. Executive Summary
AsWritten is a CLI whose unit of work is a **claimed extract vs file bytes**. A quote, a fixture, a "verbatim" regex copied out of a source file is a hypothesis. The tool reads the file as bytes, not as a rendered line, and either **certifies** the claim or lists the controls that `sed`/`diff`/the terminal will drop. The novel claim: **reading a file is not traversing it.**

## 2. Prior Art Landscape
`xxd`, `od`, `hexdump` dump. `cat -v` renders. `diff` compares after locale decoding. None of them take a human's "this is the line" and fail because a U+0008 sat in the capture group. Bram's 11/11 fixture today certified a predicate the artifact could not match.

## 3. Core Novelty Thesis
A verbatim claim is a typed object with two instruments: the snippet and the file. If they differ in bytes the renderers hide, the claim is false — not "looks the same." AsWritten makes that grammar executable.

Surprising turn: invert hexdump. Dumping bytes is looking. Certifying a quote against bytes is **refusing the pretty line**.

## 4. Full Exposition
Subcommands: `controls <file>` (list C0/C1 with offset, line, a render-warning); `certify <file> --claim-file <path>` or `--claim -` (exit 0 only if the claim's bytes are a slice of the file bytes). Stdlib. Exit 0 match; 2 missing file; 3 claim not found as bytes; 4 controls present (optional `--fail-on-control`); 64 usage. No `[OK]`.

## 5. Cross-Domain Synthesis Evidence
Primary: CLI / agent tooling.

| domain | insight | applied as |
|---|---|---|
| Notary | stamp is on this document | claim must be a byte slice, not a lookalike |
| Photography (RAW vs JPEG) | preview is not the negative | rendered line is JPEG; file is RAW |
| TCP checksum | the wire image, not the print | compare bytes, not unicode string |
| Court exhibit | testimony ≠ exhibit | `--claim` is testimony; file is exhibit |
| Immunology | specific epitope | U+0008 is the epitope sed cannot present |
| Double-entry | debit without credit | a quote without a byte match is unbalanced |

Structurally integrated: RAW vs JPEG + notary stamp. Synthesis 8/10.

## 6. Adversarial Gauntlet
**Primary:** "This is hexdump with extra flags."
→ Defeated: hexdump has no certify-against-claim; it cannot fail a fixture that dropped a backspace.

**Secondary:**
1. "`cat -v` already shows controls." → it renders; it does not bind a claim to a slice.
2. "`diff` would have caught it." → today's incident: diff displayed nothing for U+0008.
3. "Agents can `open(file,'rb')`." → they did, then transcribed. The tool is the refuse-to-transcribe primitive.

Falsifiable: write a file containing `BACKSPACE` in a regex; certify a claim without that byte; expect exit 3. `controls` must list U+0008.

## 7. Boundary Conditions
- UTF-8 multibyte is not C0; we do not flag combining marks unless asked (`--all-non-ascii` later).
- A claim larger than the file always fails 3.
- Binary files: `controls` still works; certify is bytewise, fine.
- Does not prove "this is the regex the process loaded" — only "this claim is in this file." Process image is out of scope.

## 8. Novelty Scoring Rubric
| dimension | max | score | why |
|---|---|---|---|
| Core absent | 10 | 8 | certify-against-bytes not found in xxd/cat -v/diff |
| Unrelated ideas | 10 | 7 | RAW vs JPEG + notary |
| Surprise | 10 | 8 | dump inverted into refuse-the-pretty-line |
| Arrangement | 15 | 11 | claim/file as hop-pair cousin of Arrived, different job |
| Methodology | 10 | 7 | fail-on-hidden-control |
| Field constraints | 10 | 8 | stdlib CLI, no [OK] |
| Advances field | 10 | 9 | today's exact family failure |
| Survives critique | 10 | 8 | primary named |
| Non-obvious | 5 | 4 | from a live incident, not a brainstorm |
| Synthesis | 10 | 7 | two insights in exit codes |
| **TOTAL** | **100** | **77** | GENUINELY NOVEL |

STANDARD bar 70: PASS.

## 9. Novelty Transparency Manifest
- **Novel:** claim-as-hypothesis; certify against raw bytes; render-warning on C0.
- **Foundational:** pathlib, argparse, byte scan.
- **Origin:** Bram 2026-09-05 U+0008 in the loop-key regex; sed/diff ate the byte; 11/11 on a transcription.
- **Surprise:** a passing visual diff is the failure mode.

## Appendix D
1. Reject obvious (`xxd`/`cat -v`) — dump ≠ certify. PASS.
2. Synthesis: RAW vs JPEG + notary. PASS.
3. Cliché named: "hexdump CLI." Avoided. PASS.
4. Critic defeated. PASS.
5. Score 77. PASS.
