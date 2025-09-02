import shlex
from typing import Optional
from .vfs import VFS
from .commands import Commands, COMMAND_MAP, CommandError

class Shell:
    def __init__(self, vfs: VFS):
        self.vfs = vfs
        self.cwd = '/'
        self.history = []
        self.commands = Commands(vfs, self)
        self.running = True

    def resolve_path(self, path: str) -> str:
        if path.startswith('/'):
            curpath = path
        else:
            curpath = self.cwd.rstrip('/') + '/' + path
        parts = []
        for p in curpath.split('/'):
            if p in ('', '.'):
                continue
            if p == '..':
                if parts:
                    parts.pop()
            else:
                parts.append(p)
        return '/' + '/'.join(parts)

    def execute_line(self, line: str) -> str:
        try:
            args = shlex.split(line)
        except ValueError as e:
            return f'Parse error: {e}'
        if not args:
            return ''
        cmd, *cmd_args = args
        self.history.append(line)
        if cmd == 'exit':
            self.running = False
            return ''
        handler = COMMAND_MAP.get(cmd)
        if not handler:
            return f'Unknown command: {cmd}'
        try:
            output = handler(self.commands, cmd_args)
            return output
        except CommandError as e:
            return str(e)
