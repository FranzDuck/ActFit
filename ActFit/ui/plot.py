import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
import tkinter.ttk as ttk
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.backend_bases import key_press_handler as mpl_key_press_handler


__all__ = ("Plot",)


class Plot(ttk.Frame):
    def __init__(self, master=None, figsize=None, dpi=None, **kw):
        super().__init__(master=master, **kw)

        self._fig = Figure(figsize=figsize or (5, 4), dpi=dpi or 100)
        self._ax = self._fig.add_subplot(111)
        self._fit_plot = None
        self._data_plot = None

        self._build_canvas()

    def _build_canvas(self):
        self._canvas = FigureCanvasTkAgg(self._fig, master=self)
        self._canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self._canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self._canvas.mpl_connect("key_press_event", self._key_press_handler)

    def _key_press_handler(self, event):
        mpl_key_press_handler(event, self._canvas)

    def reset(self):
        if hasattr(self, "_canvas"):
            self._canvas.get_tk_widget().destroy()
        self._build_canvas()

    def plot(self):
        try:
            if self.master.plot_ready:
                xs = self.master.xs

                data_ys = self.master.data
                if not self._data_plot:
                    self._data_plot = self._ax.scatter(
                        xs, data_ys, marker="x", color="darkorange"
                    )
                else:
                    self._data_plot.set_offsets(np.column_stack((xs, data_ys)))

                fit_ys = self.master.ys
                if not self._fit_plot:
                    self._fit_plot, *_ = self._ax.plot(xs, fit_ys, color="steelblue")
                else:
                    self._fit_plot.set_data(xs, fit_ys)

                all_ys = np.array([*fit_ys, *data_ys])
                left, right = np.min(all_ys) - 1, np.max(all_ys) + 1
                self._ax.set_ylim([left, right])

                left, right = np.min(xs) - 1, np.max(xs) + 1
                self._ax.set_xlim([left, right])

                self._ax.grid(True)
                self._canvas.draw()
        except Exception as e:
            messagebox.showerror(type(e).__name__, e.args[0])
            raise e
