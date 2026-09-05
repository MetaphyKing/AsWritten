# AsWritten

A stdlib CLI. **Reading a file is not traversing it.**

`controls` lists C0 bytes that `sed`/`diff` will hide (BACKSPACE named).
`certify` treats a quote as a hypothesis: it must be a contiguous **byte slice** of the file.

## Install (stranger path)

1. Install Python 3.10 or newer. No pip packages.
2. Copy this folder. `cd` into it.
3. `python -m unittest test_aswritten.py`
4. Copy a command from `EXAMPLES.md`.

```
python aswritten.py controls src.js
python aswritten.py certify src.js --claim-file quote.txt
python aswritten.py certify src.txt --claim-text "beta"
```

`--chunk N` uses a sliding window (claims may span chunks).

## Exit codes
0 ok · 2 missing file · 3 claim not in file · 64 usage

## Test
```
python -m unittest test_aswritten.py
```

## Team Brain

Before you publish "the regex is this" or a fixture labelled verbatim, run `controls` on the file and `certify` the quote against the file **bytes**. If `sed`/`diff` showed nothing, `controls` still will. Today's loop-key U+0008 is the specimen.

### Artifact/AsWritten card (Task 5)

`Artifact/AsWritten` — CLI that certifies a claimed extract against file bytes and lists C0 controls that renderers hide. Stdlib. No `[OK]`.
Related: VariantCollator; `wake\tools\ctlscan.js`.
