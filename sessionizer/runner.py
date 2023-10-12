import subprocess


def run_workspace(project, timeout=None):
    results = []
    for command in project["commands"]:
        completed = subprocess.run(command, cwd=project["directory"], timeout=timeout,
                                   check=False)
        results.append({"command": command, "returncode": completed.returncode})
        if completed.returncode:
            break
    return results
