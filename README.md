# sessionizer

Keep named terminal workspaces in a small JSON file and launch their commands without a shell.

## Quick start

Python 3.9 or newer. Works with ordinary executables on macOS and Linux.

```sh
python3 -m sessionizer --config examples/workspaces.json list
python3 -m sessionizer --config examples/workspaces.json show notes
python3 -m sessionizer --config examples/workspaces.json doctor notes
python3 -m sessionizer --config examples/workspaces.json run notes
```

Copy the example to `~/.config/sessionizer.json` for the default configuration.
Paths are relative to the configuration file. `run` executes argument arrays
without shell expansion and stops at the first failed command. Use `--timeout`
after the workspace name to change the per-command timeout (default 300 seconds).
Exit codes: 0 success, 1 command failure, 2 bad configuration, 124 timeout.

`tmux NAME` creates a detached session with one window per command. Install tmux
separately and attach with `tmux attach -t NAME`. Existing sessions are left alone.
Only trusted configurations should be used: commands run with your permissions.
The runner is not a sandbox. It does not supervise daemon processes or kill an
entire process tree on timeout. tmux windows close when their command exits.

## Checks

```sh
python3 -m pip install -r requirements-dev.txt
make test
make lint
```

Tests execute short-lived Python commands in temporary directories. They do not
open terminals or require tmux. The optional tmux integration needs a manual test
on a machine with tmux installed.
