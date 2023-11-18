import subprocess
import sys
import unittest


class CliTests(unittest.TestCase):
    def test_example(self):
        args = [sys.executable, "-m", "sessionizer", "--config", "examples/workspaces.json"]
        listing = subprocess.run(args + ["list"], capture_output=True, text=True)
        self.assertEqual(listing.stdout.strip(), "notes")
        run = subprocess.run(args + ["run", "notes"], capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(run.stdout.strip(), "Workspace ready")

    def test_invalid_tmux_name(self):
        from sessionizer.tmux import tmux_workspace
        with self.assertRaises(ValueError):
            tmux_workspace("bad:name", {"directory": ".", "commands": []})
