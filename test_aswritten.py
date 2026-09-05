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


class V2(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.d = Path(self.tmp.name)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_controls_backspace(self) -> None:
        p = self.d / "src.js"
        p.write_bytes(b"const K = /foo[\x08]/\n")
        r = run(["controls", str(p)])
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("BACKSPACE", r.stdout)
        self.assertNotIn("[OK]", r.stdout)

    def test_certify_file(self) -> None:
        src = self.d / "src.txt"
        src.write_bytes(b"hello NEEDLE world")
        claim = self.d / "c.txt"
        claim.write_bytes(b"NEEDLE")
        r = run(["certify", str(src), "--claim-file", str(claim)])
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("CERTIFIED", r.stdout)

    def test_certify_text(self) -> None:
        src = self.d / "src.txt"
        src.write_bytes(b"alpha beta gamma")
        r = run(["certify", str(src), "--claim-text", "beta"])
        self.assertEqual(r.returncode, 0)

    def test_transcription_drop(self) -> None:
        src = self.d / "src.js"
        src.write_bytes(b"const AIT_KEY = /foo[\x08]/\n")
        claim = self.d / "c.txt"
        claim.write_bytes(b"const AIT_KEY = /foo[]/\n")
        r = run(["certify", str(src), "--claim-file", str(claim)])
        self.assertEqual(r.returncode, 3)

    def test_span_chunks(self) -> None:
        src = self.d / "src.bin"
        src.write_bytes(b"aaaNEEDLEbbb")
        claim = self.d / "c.bin"
        claim.write_bytes(b"NEEDLE")
        r = run(["certify", str(src), "--claim-file", str(claim), "--chunk", "4"])
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_missing(self) -> None:
        self.assertEqual(run(["controls", str(self.d / "nope")]).returncode, 2)

    def test_usage(self) -> None:
        self.assertEqual(run([]).returncode, 64)
        self.assertEqual(run(["certify", "x"]).returncode, 64)


if __name__ == "__main__":
    unittest.main()
