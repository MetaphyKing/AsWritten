#!/usr/bin/env python3
"""AsWritten v2 — combined.

controls: list hidden C0 bytes (chunked; default chunk 64KiB).
certify: claim must be a contiguous byte slice of the file
         (--claim-file and/or --claim-text; sliding window).
Reading a file is not traversing it. No [OK].
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

EX_OK, EX_MISSING, EX_NOTFOUND, EX_USAGE = 0, 2, 3, 64
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
                    print(
                        "CONTROL offset=%d line=%d col=%d byte=0x%02x name=%s hidden=yes"
                        % (offset, line, col, b, NAMES.get(b, "C0"))
                    )
                    n += 1
                if b == 0x0A:
                    line += 1
                    col = 1
                else:
                    col += 1
                offset += 1
    print("CONTROLS count=%d" % n)
    return EX_OK


def cmd_certify(path: Path, claim: bytes, chunk: int) -> int:
    if not claim:
        print("NOT_CERTIFIED reason=empty_claim")
        return EX_NOTFOUND
    try:
        fh = path.open("rb")
    except OSError:
        print("NOT_CERTIFIED reason=missing_file")
        return EX_MISSING
    overlap = max(len(claim) - 1, 0)
    prev = b""
    with fh:
        while True:
            buf = fh.read(chunk)
            if not buf:
                break
            window = prev + buf
            if window.find(claim) >= 0:
                print("CERTIFIED bytes=%d" % len(claim))
                return EX_OK
            prev = window[-overlap:] if overlap else b""
    print("NOT_CERTIFIED reason=claim_not_in_file")
    return EX_NOTFOUND


def parse_args(argv: list[str] | None) -> argparse.Namespace | int:
    ap = argparse.ArgumentParser(prog="aswritten", exit_on_error=False)
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("controls")
    c.add_argument("file")
    c.add_argument("--chunk", type=int, default=65536)
    y = sub.add_parser("certify")
    y.add_argument("file")
    y.add_argument("--claim-file", default="")
    y.add_argument("--claim-text", default="")
    y.add_argument("--chunk", type=int, default=65536)
    try:
        args = ap.parse_args(argv)
    except (argparse.ArgumentError, SystemExit):
        return EX_USAGE
    if args.cmd == "certify" and not args.claim_file and not args.claim_text:
        return EX_USAGE
    if getattr(args, "chunk", 1) < 1:
        return EX_USAGE
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if isinstance(args, int):
        print("NOT_CERTIFIED reason=usage")
        return args
    path = Path(args.file)
    if args.cmd == "controls":
        return cmd_controls(path, args.chunk)
    claim = b""
    if args.claim_file:
        try:
            claim = Path(args.claim_file).read_bytes()
        except OSError:
            print("NOT_CERTIFIED reason=missing_claim")
            return EX_MISSING
    if args.claim_text:
        extra = args.claim_text.encode("utf-8")
        claim = extra if not claim else claim + extra
    return cmd_certify(path, claim, args.chunk)


if __name__ == "__main__":
    raise SystemExit(main())
