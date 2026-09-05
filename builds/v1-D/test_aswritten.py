#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

PY = sys.executable
SCRIPT = Path(__file__).resolve().parent / "aswritten.py"


def run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [PY, str(SCRIPT), *args],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )


class D(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.d = Path(self.tmp.name)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_span_chunks(self) -> None:
        src = self.d / "src.bin"
        src.write_bytes(b"aaaNEEDLEbbb")
        claim = self.d / "c.bin"
        claim.write_bytes(b"NEEDLE")
        r = run(["certify", str(src), "--claim-file", str(claim), "--chunk", "4"])
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("CERTIFIED", r.stdout)

    def test_not_found(self) -> None:
        src = self.d / "src.bin"
        src.write_bytes(b"aaa")
        claim = self.d / "c.bin"
        claim.write_bytes(b"NEEDLE")
        r = run(["certify", str(src), "--claim-file", str(claim), "--chunk", "2"])
        self.assertEqual(r.returncode, 3)

    def test_usage(self) -> None:
        self.assertEqual(run([]).returncode, 64)


if __name__ == "__main__":
    unittest.main()
