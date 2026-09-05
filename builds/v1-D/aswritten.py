#!/usr/bin/env python3
"""AsWritten v1-D — sliding-window certify (claim may span chunk boundaries)."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

EX_OK, EX_MISSING, EX_NOTFOUND, EX_USAGE = 0, 2, 3, 64


def certify_window(path: Path, claim: bytes, chunk: int) -> int:
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


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="aswritten", exit_on_error=False)
    sub = ap.add_subparsers(dest="cmd", required=True)
    y = sub.add_parser("certify")
    y.add_argument("file")
    y.add_argument("--claim-file", required=True)
    y.add_argument("--chunk", type=int, default=65536)
    try:
        args = ap.parse_args(argv)
    except (argparse.ArgumentError, SystemExit):
        print("NOT_CERTIFIED reason=usage")
        return EX_USAGE
    if args.chunk < 1:
        print("NOT_CERTIFIED reason=usage")
        return EX_USAGE
    try:
        claim = Path(args.claim_file).read_bytes()
    except OSError:
        print("NOT_CERTIFIED reason=missing_claim")
        return EX_MISSING
    return certify_window(Path(args.file), claim, args.chunk)


if __name__ == "__main__":
    raise SystemExit(main())
