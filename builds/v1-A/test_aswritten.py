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


class A(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.d = Path(self.tmp.name)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_controls_backspace(self) -> None:
        p = self.d / "src.js"
        p.write_bytes(b"const AIT_KEY = /foo[\x08]/\n")
        r = run(["controls", str(p)])
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("name=BACKSPACE", r.stdout)
        self.assertIn("hidden=yes", r.stdout)
        self.assertNotIn("[OK]", r.stdout)

    def test_certify_ok(self) -> None:
        src = self.d / "src.txt"
        src.write_bytes(b"hello BACKSPACE world")
        claim = self.d / "claim.txt"
        claim.write_bytes(b"BACKSPACE")
        r = run(["certify", str(src), "--claim-file", str(claim)])
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("CERTIFIED", r.stdout)

    def test_certify_missing_byte(self) -> None:
        src = self.d / "src.txt"
        src.write_bytes(b"const AIT_KEY = /foo[\x08]/\n")
        claim = self.d / "claim.txt"
        claim.write_bytes(b"const AIT_KEY = /foo[]/\n")  # transcription dropped BS
        r = run(["certify", str(src), "--claim-file", str(claim)])
        self.assertEqual(r.returncode, 3)
        self.assertIn("claim_not_in_file", r.stdout)

    def test_missing_file(self) -> None:
        r = run(["controls", str(self.d / "nope")])
        self.assertEqual(r.returncode, 2)

    def test_usage(self) -> None:
        r = run([])
        self.assertEqual(r.returncode, 64)


if __name__ == "__main__":
    unittest.main()
