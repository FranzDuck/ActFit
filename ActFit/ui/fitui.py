import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk

import numpy as np
import scipy.optimize as opt

from ..fit import Fit
from .param_slider import ParamSlider
from .utils import *


__all__ = ("FitUI",)


class FitUI(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._slider_frame = ttk.Frame(self)
        self._slider_frame.pack(fill=tk.BOTH, expand=True)
        self._sliders = dict()

        button = ttk.Button(self, text="Fit", command=event_wrapper(self.perform_fit))
        button.pack(fill=tk.X, expand=True)

    @property
    def params(self):
        return {key: slider.value for key, slider in self._sliders.items()}

    @property
    def boundaries(self):
        return {key: slider.boundary for key, slider in self._sliders.items()}

    def update(self):
        for slider in self._sliders.values():
            slider.destroy()
        self._sliders = dict()
        if self.master.func is not None:
            for i, param in enumerate(self.master.func.__code__.co_varnames[1:]):
                self._sliders[param] = slider = ParamSlider(self._slider_frame, param)
                slider.grid(row=i, column=0, sticky="ew")
        self.event_generate("<<FITUI.UPDATED>>")

    def perform_fit(self):
        params, cov = opt.curve_fit(
            self.master.func,
            self.master.xs,
            self.master.data,
            p0=list(self.params.values()),
            bounds=[
                [v for v, _ in self.boundaries.values()],
                [v for _, v in self.boundaries.values()],
            ],
        )
        for name, value in zip(self._sliders, params):
            self._sliders[name].set_scale_value(value)
        self.event_generate("<<FITUI.DONE>>")
