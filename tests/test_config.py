import json
import tempfile
import unittest
from pathlib import Path
from sessionizer.config import load


class ConfigTests(unittest.TestCase):
    def test_relative_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "config.json"
            path.write_text(json.dumps({"one": {"directory": ".", "commands": [["echo", "x"]]}}))
            self.assertEqual(load(path)["one"]["directory"], str(Path(tmp).resolve()))

    def test_shell_string_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "config.json"
            path.write_text(json.dumps({"one": {"directory": ".", "commands": ["echo x"]}}))
            with self.assertRaises(ValueError):
                load(path)

    def test_missing_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "config.json"
            path.write_text(json.dumps({"one": {"directory": "absent"}}))
            with self.assertRaises(ValueError):
                load(path)

    def test_unknown_setting(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "config.json"
            path.write_text(json.dumps({"one": {"directory": ".", "command": []}}))
            with self.assertRaisesRegex(ValueError, "Unknown setting"):
                load(path)
