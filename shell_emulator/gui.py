import tkinter as tk
from tkinter import scrolledtext
from .shell import Shell

class App:
    def __init__(self, root: tk.Tk, shell: Shell):
        self.root = root
        self.shell = shell
        self.text = scrolledtext.ScrolledText(root, state='disabled', width=80, height=24)
        self.text.pack(fill=tk.BOTH, expand=True)
        self.entry = tk.Entry(root)
        self.entry.pack(fill=tk.X)
        self.entry.bind('<Return>', self.on_enter)
        self.prompt()

    def prompt(self):
        self.append(f"{self.shell.cwd}$ ")

    def append(self, s: str):
        self.text.configure(state='normal')
        self.text.insert(tk.END, s)
        self.text.see(tk.END)
        self.text.configure(state='disabled')

    def on_enter(self, event=None):
        cmd = self.entry.get()
        self.entry.delete(0, tk.END)
        self.append(cmd + '\n')
        output = self.shell.execute_line(cmd)
        if output:
            self.append(output + '\n')
        if self.shell.running:
            self.prompt()
        else:
            self.root.quit()

def run_script(shell: Shell, app: App, path: str):
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n')
            if not line:
                continue
            app.append(f"{shell.cwd}$ {line}\n")
            output = shell.execute_line(line)
            if output:
                app.append(output + '\n')
            if not shell.running:
                break
        if shell.running:
            app.prompt()
