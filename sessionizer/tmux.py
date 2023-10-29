import re
import shlex
import subprocess


def tmux_workspace(name, project):
    if not re.fullmatch(r"[A-Za-z0-9_-]+", name):
        raise ValueError("tmux names may contain letters digits hyphens and underscores")
    if subprocess.run(["tmux", "has-session", "-t", "=" + name],
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0:
        raise ValueError("tmux session already exists")
    commands = project["commands"] or [[]]
    for index, command in enumerate(commands):
        args = (["tmux", "new-session", "-d", "-s", name] if index == 0 else
                ["tmux", "new-window", "-t", name])
        args.extend(["-c", project["directory"]])
        if command:
            args.append("exec " + shlex.join(command))
        subprocess.run(args, check=True)
