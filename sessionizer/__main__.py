import argparse
import json
import subprocess
import sys
from pathlib import Path
from .config import load
from .runner import run_workspace
from .doctor import doctor


def main():
    parser = argparse.ArgumentParser(description="Named terminal workspaces")
    parser.add_argument("--config", type=Path, default=Path.home() / ".config/sessionizer.json")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("list")
    for name in ("show", "run", "doctor"):
        command = commands.add_parser(name)
        command.add_argument("name")
        if name == "run":
            command.add_argument("--timeout", type=float, default=300)
    args = parser.parse_args()
    try:
        projects = load(args.config)
        if args.command == "list":
            print("\n".join(sorted(projects)))
            return 0
        if args.name not in projects:
            raise ValueError("Unknown workspace: " + args.name)
        project = projects[args.name]
        if args.command == "show":
            print(json.dumps(project, indent=2))
            return 0
        if args.command == "doctor":
            issues = doctor(project)
            print("\n".join(issues) if issues else "Workspace is ready")
            return int(bool(issues))
        if args.timeout <= 0:
            raise ValueError("Timeout must be positive")
        results = run_workspace(project, args.timeout)
        return 1 if any(item["returncode"] for item in results) else 0
    except subprocess.TimeoutExpired:
        print("Workspace command timed out", file=sys.stderr)
        return 124
    except (OSError, ValueError) as error:
        print(str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
