import json
from pathlib import Path


def load(path):
    path = Path(path)
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Configuration must be an object")
    projects = {}
    for name, project in data.items():
        if not isinstance(name, str) or not name or not isinstance(project, dict):
            raise ValueError("Invalid workspace entry")
        directory = project.get("directory")
        if not isinstance(directory, str) or not directory:
            raise ValueError("Workspace %s needs a directory" % name)
        directory = Path(directory).expanduser()
        if not directory.is_absolute():
            directory = path.resolve().parent / directory
        directory = directory.resolve()
        if not directory.is_dir():
            raise ValueError("Workspace %s directory does not exist" % name)
        projects[name] = {"directory": str(directory), "commands": project.get("commands", [])}
    return projects
