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


class C(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.d = Path(self.tmp.name)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_chunked_backspace(self) -> None:
        p = self.d / "s.bin"
        p.write_bytes(b"xxxx\x08yyyy")
        r = run(["controls", str(p), "--chunk", "3"])
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("BACKSPACE", r.stdout)
        self.assertIn("offset=4", r.stdout)

    def test_missing(self) -> None:
        self.assertEqual(run(["controls", str(self.d / "nope")]).returncode, 2)

    def test_usage(self) -> None:
        self.assertEqual(run([]).returncode, 64)


if __name__ == "__main__":
    unittest.main()
