import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from sessionizer.runner import run_workspace
from sessionizer.doctor import doctor


class RunnerTests(unittest.TestCase):
    def test_runs_in_workspace(self):
        with tempfile.TemporaryDirectory() as tmp:
            code = "from pathlib import Path; Path('result').write_text('done')"
            project = {"directory": tmp, "commands": [[sys.executable, "-c", code]]}
            self.assertEqual(run_workspace(project)[0]["returncode"], 0)
            self.assertEqual((Path(tmp) / "result").read_text(), "done")

    def test_stops_on_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            commands = [[sys.executable, "-c", "raise SystemExit(7)"], ["missing-command"]]
            result = run_workspace({"directory": tmp, "commands": commands})
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]["returncode"], 7)

    def test_timeout(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = {"directory": tmp,
                       "commands": [[sys.executable, "-c", "import time; time.sleep(10)"]]}
            with self.assertRaises(subprocess.TimeoutExpired):
                run_workspace(project, 0.05)

    def test_doctor(self):
        self.assertEqual(doctor({"directory": ".", "commands": [[sys.executable]]}), [])
        self.assertEqual(len(doctor({"directory": ".", "commands": [["missing-command"]]})), 1)
