import tkinter as tk
import tkinter.ttk as ttk

from .utils import *


__all__ = ("ParamSlider",)


class ParamSlider(ttk.Frame):
    def __init__(self, root, label, *args, **kwargs):
        super().__init__(root, *args, **kwargs)

        self._name = label

        label = ttk.Label(self, text=label + " = ", font=MONOSPACE_FONT, anchor="e")
        label.grid(row=0, column=0, sticky="w")

        self._lower_bound = tk.StringVar()
        self._lower_bound.set("0")
        self._lower_bound.trace("w", self._update_value)
        lower_bound_entry = tk.Entry(
            self, width=5, justify=tk.RIGHT, textvariable=self._lower_bound
        )
        lower_bound_entry.grid(row=0, column=1, sticky="nse")

        self._scale = ttk.Scale(
            self, from_=1, to=100, orient=tk.HORIZONTAL, command=self._update_value
        )
        self._scale.grid(row=0, column=2, columnspan=2, sticky="ew")

        self._upper_bound = tk.StringVar()
        self._upper_bound.set("10")
        self._upper_bound.trace("w", self._update_value)
        upper_bound_entry = tk.Entry(
            self, width=5, justify=tk.RIGHT, textvariable=self._upper_bound
        )
        upper_bound_entry.grid(row=0, column=4, sticky="nse")

        self._value = 1.0
        self._value_str = tk.StringVar()
        self._value_str.set(" = ")
        value_label = ttk.Label(
            self, textvariable=self._value_str, font=MONOSPACE_FONT, anchor="e"
        )
        value_label.grid(row=0, column=5, sticky="w")

        self.set_value(1)

    @property
    def value(self):
        return self._value

    @property
    def boundary(self):
        return (float(self._lower_bound.get()), float(self._upper_bound.get()))

    def set_value(self, x):
        y1, y2 = self.boundary
        self._value = y1 + (x - 1) * (y2 - y1) / 99
        self._value_str.set(f" = {self._value: >+4.3f}")

    def set_scale_value(self, x):
        self._value = x
        self._value_str.set(f" = {self._value: >+4.3f}")
        y1, y2 = self.boundary
        self._scale.set(1 + (x - y1) * 99 / (y2 - y1))

    def _update_value(self, *args):
        self.set_value(self._scale.get())
        self.event_generate("<<PARAM.UPDATED>>")
