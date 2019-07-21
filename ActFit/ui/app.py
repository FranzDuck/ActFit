import argparse as argp
from copy import copy
import inspect
import tkinter as tk
from tkinter import messagebox, filedialog
import tkinter.ttk as ttk

import numpy as np
import scipy.optimize as opt


from .env import Env
from .param_slider import ParamSlider
from .plot import Plot
from .fitui import FitUI
from .utils import *


class App(ttk.Frame):
    def __init__(self, *args, src=None, **kwargs):
        super().__init__(*args, **kwargs)

        self._env = Env(globals_={"np": np})

        menubar = tk.Menu(self)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Save Fit", command=event_wrapper(self._save_fit))
        file_menu.add_separator()
        file_menu.add_command(
            label="Load Source", command=event_wrapper(self._load_source)
        )
        file_menu.add_command(
            label="Save Source", command=event_wrapper(self._save_source)
        )
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Usage", command=event_wrapper(self._spawn_usage))
        help_menu.add_command(label="About", command=event_wrapper(self._spawn_about))
        menubar.add_cascade(label="Help", menu=help_menu)

        self.master.config(menu=menubar)

        self._src = self._env.build_src_view(self)
        self._src.pack(fill=tk.BOTH, expand=True)
        self._src.populate(src)

        picker_frame = ttk.Frame(self)
        picker_frame.pack(fill=tk.BOTH, expand=True)

        self._fitui = FitUI(self)
        self._fitui.pack(fill=tk.BOTH, expand=True)

        self._plot = Plot(self)
        self._plot.pack(fill=tk.BOTH, expand=True)

        self._func_choice = self._env.build_picker(
            picker_frame, "Function", callable_=True, command=self._fitui.update
        )
        self._func_choice.grid(column=0, row=2, sticky="ew")

        self._xs_choice = self._env.build_picker(
            picker_frame, "Space", callable_=False, command=self._plot.plot
        )
        self._xs_choice.grid(column=1, row=2, sticky="ew")

        self._data_choice = self._env.build_picker(
            picker_frame, "Data", callable_=False, command=self._plot.plot
        )
        self._data_choice.grid(column=2, row=2, sticky="ew")

        self.bind_all("<<SOURCE.DONE>>", event_wrapper(self._plot.reset), add="+")
        self.bind_all("<<SOURCE.RESET>>", event_wrapper(self._plot.reset), add="+")
        self.bind_all("<<FITUI.UPDATED>>", event_wrapper(self._plot.plot), add="+")
        self.bind_all("<<PARAM.UPDATED>>", event_wrapper(self._plot.plot), add="+")
        self.bind_all("<<FITUI.DONE>>", event_wrapper(self._plot.plot), add="+")
        self.bind_all(
            "<<PICKER.CHOSEN.Space>>", event_wrapper(self._plot.plot), add="+"
        )
        self.bind_all("<<PICKER.CHOSEN.Data>>", event_wrapper(self._plot.plot), add="+")
        self.bind_all(
            "<<PICKER.CHOSEN.Function>>",
            event_wrapper(chain_call(self._fitui.update, self._plot.plot)),
            add="+",
        )

        self._src.run()
        self._fitui.update()

    def _save_fit(self):
        ...

    def _load_source(self):
        path = filedialog.askopenfilename(
            master=self, filetypes=[("Python files", "*.py"), ("All files", "*")]
        )
        if path:
            with open(path, "r") as f:
                self._src.populate(f.read())

    def _save_source(self):
        path = filedialog.asksaveasfilename(
            master=self, filetypes=[("Python files", "*.py"), ("All files", "*")]
        )
        if path:
            with open(path, "w") as f:
                f.write(self._src.text)

    def _spawn_usage(self):
        ...

    def _spawn_about(self):
        ...

    @property
    def params(self):
        return self._fitui.params

    @property
    def func(self):
        return self._func_choice.value

    @property
    def ys(self):
        if self.xs is None or self.func is None:
            return None
        return self.func(self.xs, **self.params)

    @property
    def xs(self):
        return self._xs_choice.value

    @property
    def data(self):
        return self._data_choice.value

    @property
    def plot_ready(self):
        return self.func is not None and self.xs is not None and self.data is not None

    @classmethod
    def run_from_cmd(cls):
        parser = argp.ArgumentParser()

        args = parser.parse_args()

        cls.run()

    @classmethod
    def run(cls, **kwargs):
        root = tk.Tk()
        root.resizable(0, 0)
        root.title("ActFit")
        s = ttk.Style(root)
        s.theme_use("clam")
        app = cls(root, **kwargs)
        app.pack(fill=tk.BOTH, expand=True)
        app.mainloop()


if __name__ == "__main__":
    App.run(
        src="""import numpy as np

def f(xs, m, b, c):
    return m * np.sin(b * xs) + c

xs = np.linspace(0, np.pi*2, 100)

data = np.sin(xs) + np.random.rand(100)*3"""
    )

