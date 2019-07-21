import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
import tkinter.ttk as ttk


from .utils import *


__all__ = ("Env",)


class Env:
    def __init__(self, globals_=None):
        self._pickers = []
        self._original_globals = globals_ or {}
        self.reset()

    def reset(self):
        self._globals = self._original_globals
        self.locals = {}
        self.callables = []
        self.non_callables = []
        for picker in self._pickers:
            picker.clear()

    def exec(self, code):
        exec(code, self._globals, self.locals)
        self.callables = [key for key, value in self.locals.items() if callable(value)]
        self.non_callables = [
            key for key, value in self.locals.items() if not callable(value)
        ]
        for picker in self._pickers:
            picker.update()

    def eval(self, code):
        return eval(code, self._globals, self.locals)

    def __getitem__(self, key):
        return self.locals[key]

    def get(self, key, default=None):
        return self.locals.get(key, default)

    def build_src_view(self, master):
        class SourceView(ttk.Frame):
            def __init__(self, env, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self._env = env

                self._text = ScrolledText(self, height=10, width=70)
                self._text.config(font=MONOSPACE_FONT, undo=True, wrap="word")
                self._text.grid(row=0, column=0, columnspan=6, sticky="nsew")

                self._run_button = ttk.Button(
                    self, text="Run", command=event_wrapper(self.run)
                )
                self._run_button.grid(column=0, row=1, columnspan=3, sticky="ew")
                self._reset_button = ttk.Button(
                    self, text="Reset", command=event_wrapper(self.reset)
                )
                self._reset_button.grid(column=3, row=1, columnspan=3, sticky="ew")

            @property
            def text(self):
                return self._text.get("1.0", "end-1c")

            def run(self):
                try:
                    self._env.exec(self.text)
                except Exception as e:
                    messagebox.showwarning(type(e).__name__, e.args[0])
                self.event_generate("<<SOURCE.DONE>>")

            def reset(self):
                self._text.delete("1.0", tk.END)
                self._env.reset()
                self.event_generate("<<SOURCE.RESET>>")

            def populate(self, src):
                self._text.insert(tk.END, src)
                self.run()

        return SourceView(self, master)

    def build_picker(self, master, name, callable_=False, command=None):
        class Picker(ttk.Frame):
            def __init__(self, env, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self._env = env
                self._callable = callable_

                self._name = name

                label = ttk.Label(self, text=name + ":")
                label.grid(column=0, row=0)
                self._choice = tk.StringVar(self, "")
                self._choice_menu = ttk.OptionMenu(self, self._choice)
                self._choice_menu.grid(column=1, row=0)

                self._choice.trace("w", self._choice_taken)

            def _choice_taken(self, *args):
                self.event_generate("<<PICKER.CHOSEN>>")
                self.event_generate(f"<<PICKER.CHOSEN.{name}>>")

            def clear(self):
                self._choice.set("")
                self._choice_menu["menu"].delete(0, "end")

            def update(self):
                targets = (
                    self._env.callables if self._callable else self._env.non_callables
                )
                self.clear()
                if targets:
                    for name in targets:
                        self._choice_menu["menu"].add_command(
                            label=name, command=tk._setit(self._choice, name)
                        )
                    self._choice.set(targets[0])

            @property
            def value(self):
                return self._env.get(self._choice.get())

        picker = Picker(self, master)
        self._pickers.append(picker)
        return picker

