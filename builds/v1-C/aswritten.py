#!/usr/bin/env python3
"""AsWritten v1-C — chunked controls (does not slurp the whole file)."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

EX_OK, EX_MISSING, EX_USAGE = 0, 2, 64
HIDDEN = set(range(0x00, 0x20)) - {0x09, 0x0A, 0x0D}
HIDDEN.add(0x7F)
NAMES = {0: "NUL", 8: "BACKSPACE", 11: "VT", 12: "FF", 27: "ESC", 127: "DEL"}


def cmd_controls(path: Path, chunk: int) -> int:
    try:
        fh = path.open("rb")
    except OSError:
        print("NOT_CERTIFIED reason=missing_file")
        return EX_MISSING
    n = 0
    offset = 0
    line, col = 1, 1
    with fh:
        while True:
            buf = fh.read(chunk)
            if not buf:
                break
            for b in buf:
                if b in HIDDEN:
                    print("CONTROL offset=%d line=%d col=%d byte=0x%02x name=%s hidden=yes" % (
                        offset, line, col, b, NAMES.get(b, "C0")))
                    n += 1
                if b == 0x0A:
                    line += 1
                    col = 1
                else:
                    col += 1
                offset += 1
    print("CONTROLS count=%d" % n)
    return EX_OK


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="aswritten", exit_on_error=False)
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("controls")
    c.add_argument("file")
    c.add_argument("--chunk", type=int, default=65536)
    try:
        args = ap.parse_args(argv)
    except (argparse.ArgumentError, SystemExit):
        print("NOT_CERTIFIED reason=usage")
        return EX_USAGE
    if args.chunk < 1:
        print("NOT_CERTIFIED reason=usage")
        return EX_USAGE
    return cmd_controls(Path(args.file), args.chunk)


if __name__ == "__main__":
    raise SystemExit(main())
