# AsWritten — worked examples

Measured 2026-09-05 on this box. `ex_src.js` contains a U+0008 (BACKSPACE) inside a regex.

## 1. List hidden controls

```
python aswritten.py controls ex_src.js
```

Expected:
```
CONTROL offset=12 line=1 col=13 byte=0x08 name=BACKSPACE hidden=yes
CONTROLS count=1
```
exit 0.

## 2. Certify a transcription that dropped the byte

```
python aswritten.py certify ex_src.js --claim-file ex_claim_dropped.txt
```

Expected:
```
NOT_CERTIFIED reason=claim_not_in_file
```
exit 3. This is the sed/diff lie.

## 3. Missing file

```
python aswritten.py controls nope.bin
```

```
NOT_CERTIFIED reason=missing_file
```
exit 2. No traceback.

## 4. Usage

```
python aswritten.py
```

```
NOT_CERTIFIED reason=usage
```
exit 64.
