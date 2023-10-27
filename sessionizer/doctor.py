import os
import shutil
from pathlib import Path


def doctor(project):
    issues = []
    for command in project["commands"]:
        executable = command[0]
        if "/" in executable:
            candidate = Path(executable)
            if not candidate.is_absolute():
                candidate = Path(project["directory"]) / candidate
            found = candidate.is_file() and os.access(candidate, os.X_OK)
        else:
            found = shutil.which(executable) is not None
        if not found:
            issues.append("Executable not found: " + executable)
    return issues
