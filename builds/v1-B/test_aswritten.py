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


class B(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.d = Path(self.tmp.name)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_certify_text(self) -> None:
        p = self.d / "s.txt"
        p.write_bytes(b"alpha beta gamma")
        r = run(["certify", str(p), "--claim-text", "beta"])
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("CERTIFIED", r.stdout)

    def test_certify_fail(self) -> None:
        p = self.d / "s.txt"
        p.write_bytes(b"alpha")
        r = run(["certify", str(p), "--claim-text", "omega"])
        self.assertEqual(r.returncode, 3)

    def test_controls(self) -> None:
        p = self.d / "s.txt"
        p.write_bytes(b"a\x00b")
        r = run(["controls", str(p)])
        self.assertEqual(r.returncode, 0)
        self.assertIn("NUL", r.stdout)

    def test_usage(self) -> None:
        self.assertEqual(run([]).returncode, 64)


if __name__ == "__main__":
    unittest.main()
