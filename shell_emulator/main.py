import argparse
import tkinter as tk
from .vfs import VFS
from .shell import Shell
from .gui import App, run_script


def main():
    parser = argparse.ArgumentParser(description='Shell emulator')
    parser.add_argument('--vfs', help='Path to VFS JSON file')
    parser.add_argument('--script', help='Path to start script')
    args = parser.parse_args()

    vfs = VFS.from_json_file(args.vfs) if args.vfs else VFS()
    shell = Shell(vfs)

    root = tk.Tk()
    title = args.vfs if args.vfs else 'no VFS'
    root.title(f'Shell Emulator - {title}')
    app = App(root, shell)

    if args.script:
        run_script(shell, app, args.script)

    root.mainloop()


if __name__ == '__main__':
    main()
