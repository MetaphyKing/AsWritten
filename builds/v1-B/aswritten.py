#!/usr/bin/env python3
"""AsWritten v1-B — whole-file controls + certify --claim-text."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

EX_OK, EX_MISSING, EX_NOTFOUND, EX_USAGE = 0, 2, 3, 64
HIDDEN = set(range(0x00, 0x20)) - {0x09, 0x0A, 0x0D}
HIDDEN.add(0x7F)
NAMES = {0: "NUL", 8: "BACKSPACE", 11: "VT", 12: "FF", 27: "ESC", 127: "DEL"}


def load(path: Path) -> bytes | None:
    try:
        return path.read_bytes()
    except OSError:
        return None


def cmd_controls(path: Path) -> int:
    data = load(path)
    if data is None:
        print("NOT_CERTIFIED reason=missing_file")
        return EX_MISSING
    n = 0
    for i, b in enumerate(data):
        if b in HIDDEN:
            print("CONTROL offset=%d byte=0x%02x name=%s hidden=yes" % (
                i, b, NAMES.get(b, "C0")))
            n += 1
    print("CONTROLS count=%d" % n)
    return EX_OK


def cmd_certify(path: Path, text: str) -> int:
    data = load(path)
    if data is None:
        print("NOT_CERTIFIED reason=missing_file")
        return EX_MISSING
    claim = text.encode("utf-8")
    if not claim:
        print("NOT_CERTIFIED reason=empty_claim")
        return EX_NOTFOUND
    if data.find(claim) < 0:
        print("NOT_CERTIFIED reason=claim_not_in_file")
        return EX_NOTFOUND
    print("CERTIFIED bytes=%d" % len(claim))
    return EX_OK


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="aswritten", exit_on_error=False)
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("controls")
    c.add_argument("file")
    y = sub.add_parser("certify")
    y.add_argument("file")
    y.add_argument("--claim-text", required=True)
    try:
        args = ap.parse_args(argv)
    except (argparse.ArgumentError, SystemExit):
        print("NOT_CERTIFIED reason=usage")
        return EX_USAGE
    if args.cmd == "controls":
        return cmd_controls(Path(args.file))
    return cmd_certify(Path(args.file), args.claim_text)


if __name__ == "__main__":
    raise SystemExit(main())
