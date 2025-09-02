import calendar
import datetime
from typing import List
from .vfs import VFS

class CommandError(Exception):
    pass

class Commands:
    def __init__(self, vfs: VFS, shell: 'Shell'):
        self.vfs = vfs
        self.shell = shell

    def ls(self, args: List[str]) -> str:
        path = args[0] if args else self.shell.cwd
        abspath = self.shell.resolve_path(path)
        try:
            items = self.vfs.list_dir(abspath)
            return '\n'.join(items)
        except Exception as e:
            raise CommandError(str(e))

    def cd(self, args: List[str]) -> str:
        target = args[0] if args else '/'
        abspath = self.shell.resolve_path(target)
        try:
            node = self.vfs.get_node(abspath)
            if not isinstance(node, dict):
                raise NotADirectoryError(target)
            self.shell.cwd = abspath
            return ''
        except Exception as e:
            raise CommandError(str(e))

    def history(self, args: List[str]) -> str:
        lines = [f"{i+1} {cmd}" for i, cmd in enumerate(self.shell.history)]
        return '\n'.join(lines)

    def cal(self, args: List[str]) -> str:
        today = datetime.datetime.today()
        if len(args) == 0:
            month = today.month
            year = today.year
        elif len(args) == 1:
            month = int(args[0])
            year = today.year
        else:
            month = int(args[0])
            year = int(args[1])
        return calendar.month(year, month)

    def head(self, args: List[str]) -> str:
        if not args:
            raise CommandError('head: missing file operand')
        num = 10
        file_arg = args[0]
        if args[0] == '-n' and len(args) >= 3:
            num = int(args[1])
            file_arg = args[2]
        abspath = self.shell.resolve_path(file_arg)
        try:
            node = self.vfs.get_node(abspath)
            if isinstance(node, dict):
                raise IsADirectoryError(file_arg)
            lines = str(node).splitlines()[:num]
            return '\n'.join(lines)
        except Exception as e:
            raise CommandError(str(e))

    def touch(self, args: List[str]) -> str:
        if not args:
            raise CommandError('touch: missing file operand')
        path = self.shell.resolve_path(args[0])
        try:
            node = self.vfs.get_node(path)
            if isinstance(node, dict):
                raise IsADirectoryError(args[0])
        except FileNotFoundError:
            self.vfs.make_file(path)
        return ''

    def mkdir(self, args: List[str]) -> str:
        if not args:
            raise CommandError('mkdir: missing operand')
        path = self.shell.resolve_path(args[0])
        try:
            self.vfs.make_dir(path)
            return ''
        except Exception as e:
            raise CommandError(str(e))

COMMAND_MAP = {
    'ls': Commands.ls,
    'cd': Commands.cd,
    'history': Commands.history,
    'cal': Commands.cal,
    'head': Commands.head,
    'touch': Commands.touch,
    'mkdir': Commands.mkdir,
}
