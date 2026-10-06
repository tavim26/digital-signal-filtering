"""Tkinter dialog for choosing the filter type and its parameters."""

from __future__ import annotations

import math
import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox, ttk
from typing import NamedTuple

from signal_filtering import config
from signal_filtering.validation import Cutoff, validate_filter_parameters

PADDING = 12

FILTER_DESCRIPTIONS = {
    "lowpass": "keeps frequencies below the cutoff",
    "highpass": "keeps frequencies above the cutoff",
    "bandpass": "keeps frequencies between two cutoffs",
}


class FilterSettings(NamedTuple):
    """Filter parameters chosen by the user."""

    filter_type: str
    cutoff: Cutoff
    order: int


class FilterDialog:
    """Window that collects filter settings and validates them before closing.

    Invalid input is reported in a message box and the window stays open,
    so the user can correct it instead of restarting the application.
    """

    def __init__(self, sampling_frequency: float) -> None:
        self._sampling_frequency = sampling_frequency
        self._result: FilterSettings | None = None
        nyquist = sampling_frequency / 2

        self._root = tk.Tk()
        self._root.title("Filter Configuration")
        self._root.resizable(False, False)

        # Entries are bound to StringVars rather than DoubleVars: reading a
        # DoubleVar that holds non-numeric text raises TclError, whereas a
        # string can be parsed and the problem reported to the user.
        self._filter_type = tk.StringVar(value="lowpass")
        self._order = tk.StringVar(value=str(config.DEFAULT_FILTER_ORDER))
        self._lowpass_cutoff = tk.StringVar(
            value=f"{config.DEFAULT_LOWPASS_CUTOFF_RATIO * nyquist:g}")
        self._highpass_cutoff = tk.StringVar(
            value=f"{config.DEFAULT_HIGHPASS_CUTOFF_RATIO * nyquist:g}")
        self._bandpass_low = tk.StringVar(
            value=f"{config.DEFAULT_BANDPASS_LOW_RATIO * nyquist:g}")
        self._bandpass_high = tk.StringVar(
            value=f"{config.DEFAULT_BANDPASS_HIGH_RATIO * nyquist:g}")

        # Widgets shown only for a given filter type, keyed by type.
        self._type_specific_widgets: dict[str, list[tk.Widget]] = {}

        self._build_widgets(nyquist)
        self._show_widgets_for_selected_type()

        self._root.bind("<Return>", lambda _event: self._on_apply())
        self._root.bind("<Escape>", lambda _event: self._on_cancel())
        self._root.protocol("WM_DELETE_WINDOW", self._on_cancel)
        self._center_on_screen()

    def run(self) -> FilterSettings | None:
        """Show the window and block until it is closed.

        Returns
        -------
        FilterSettings or None
            The validated settings, or None if the user cancelled.
        """
        self._root.mainloop()
        return self._result

    # ------------------------------------------------------------------
    # Layout
    # ------------------------------------------------------------------
    def _build_widgets(self, nyquist: float) -> None:
        container = ttk.Frame(self._root, padding=PADDING)
        container.grid(sticky="nsew")

        # Keep a reference: Tk drops fonts that are garbage-collected.
        self._title_font = tkfont.nametofont("TkDefaultFont").copy()
        # A negative size means pixels rather than points; abs() is close enough.
        self._title_font.configure(
            size=abs(self._title_font.cget("size")) + 4, weight="bold")

        ttk.Label(container, text="Filter Configuration",
                  font=self._title_font).grid(row=0, column=0, sticky="w")
        ttk.Label(
            container,
            text=(f"Sampling frequency: {self._sampling_frequency:g} Hz    "
                  f"Nyquist frequency: {nyquist:g} Hz"),
        ).grid(row=1, column=0, sticky="w", pady=(2, PADDING))

        self._build_type_selector(container).grid(
            row=2, column=0, sticky="ew", pady=(0, PADDING))
        self._build_parameter_fields(container, nyquist).grid(
            row=3, column=0, sticky="ew", pady=(0, PADDING))
        self._build_buttons(container).grid(row=4, column=0, sticky="e")

    def _build_type_selector(self, parent: ttk.Frame) -> ttk.LabelFrame:
        frame = ttk.LabelFrame(parent, text="Filter type", padding=PADDING)
        for row, (key, name) in enumerate(config.FILTER_TYPES.items()):
            ttk.Radiobutton(
                frame,
                text=f"{name}: {FILTER_DESCRIPTIONS[key]}",
                value=key,
                variable=self._filter_type,
                command=self._show_widgets_for_selected_type,
            ).grid(row=row, column=0, sticky="w", pady=2)
        return frame

    def _build_parameter_fields(
        self, parent: ttk.Frame, nyquist: float
    ) -> ttk.LabelFrame:
        frame = ttk.LabelFrame(parent, text="Parameters", padding=PADDING)
        frequency_hint = f"Hz, between 0 and {nyquist:g}"

        self._add_field(
            frame, 0, "Order:",
            ttk.Spinbox(frame, from_=config.MIN_FILTER_ORDER,
                        to=config.MAX_FILTER_ORDER, increment=1,
                        textvariable=self._order, width=10),
            f"{config.MIN_FILTER_ORDER}-{config.MAX_FILTER_ORDER}, "
            "higher means a steeper roll-off",
        )

        # Rows for different filter types share the same grid rows; only the
        # rows of the selected type are visible at any time.
        self._type_specific_widgets["lowpass"] = self._add_field(
            frame, 1, "Cutoff:",
            ttk.Entry(frame, textvariable=self._lowpass_cutoff, width=12),
            frequency_hint,
        )
        self._type_specific_widgets["highpass"] = self._add_field(
            frame, 1, "Cutoff:",
            ttk.Entry(frame, textvariable=self._highpass_cutoff, width=12),
            frequency_hint,
        )
        self._type_specific_widgets["bandpass"] = self._add_field(
            frame, 1, "Lower cutoff:",
            ttk.Entry(frame, textvariable=self._bandpass_low, width=12),
            frequency_hint,
        ) + self._add_field(
            frame, 2, "Upper cutoff:",
            ttk.Entry(frame, textvariable=self._bandpass_high, width=12),
            frequency_hint,
        )
        return frame

    def _build_buttons(self, parent: ttk.Frame) -> ttk.Frame:
        frame = ttk.Frame(parent)
        ttk.Button(frame, text="Cancel", command=self._on_cancel).grid(
            row=0, column=0, padx=(0, 6))
        ttk.Button(frame, text="Apply Filter", command=self._on_apply,
                   default="active").grid(row=0, column=1)
        return frame

    @staticmethod
    def _add_field(
        parent: ttk.LabelFrame, row: int, label: str, field: tk.Widget, hint: str
    ) -> list[tk.Widget]:
        """Place a label, an input widget and a hint on one grid row."""
        widgets = [
            ttk.Label(parent, text=label),
            field,
            ttk.Label(parent, text=hint, foreground="gray"),
        ]
        for column, widget in enumerate(widgets):
            widget.grid(row=row, column=column, sticky="w", padx=(0, 8), pady=3)
        return widgets

    def _show_widgets_for_selected_type(self) -> None:
        selected = self._filter_type.get()
        for filter_type, widgets in self._type_specific_widgets.items():
            for widget in widgets:
                if filter_type == selected:
                    # grid() with no arguments restores the earlier placement.
                    widget.grid()
                else:
                    widget.grid_remove()

    def _center_on_screen(self) -> None:
        self._root.update_idletasks()
        width = self._root.winfo_reqwidth()
        height = self._root.winfo_reqheight()
        x = (self._root.winfo_screenwidth() - width) // 2
        y = (self._root.winfo_screenheight() - height) // 2
        self._root.geometry(f"+{x}+{y}")

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------
    def _on_apply(self) -> None:
        try:
            settings = self._read_settings()
            validate_filter_parameters(
                settings.filter_type, settings.cutoff,
                self._sampling_frequency, settings.order,
            )
        except ValueError as err:
            messagebox.showerror("Invalid parameters", str(err), parent=self._root)
            return
        self._result = settings
        self._root.destroy()

    def _on_cancel(self) -> None:
        self._result = None
        self._root.destroy()

    def _read_settings(self) -> FilterSettings:
        """Parse the input fields; raise ValueError on non-numeric text."""
        filter_type = self._filter_type.get()
        order = _parse_int(self._order.get(), "Filter order")
        if filter_type == "bandpass":
            cutoff: Cutoff = (
                _parse_float(self._bandpass_low.get(), "Lower cutoff"),
                _parse_float(self._bandpass_high.get(), "Upper cutoff"),
            )
        elif filter_type == "highpass":
            cutoff = _parse_float(self._highpass_cutoff.get(), "Cutoff")
        else:
            cutoff = _parse_float(self._lowpass_cutoff.get(), "Cutoff")
        return FilterSettings(filter_type, cutoff, order)


def get_filter_settings(sampling_frequency: float) -> FilterSettings | None:
    """Show the filter dialog and return the chosen settings.

    Parameters
    ----------
    sampling_frequency : float
        Sampling frequency of the loaded signal, in Hz. Used to suggest
        default cutoffs and to validate the user's input.

    Returns
    -------
    FilterSettings or None
        The validated settings, or None if the user cancelled.
    """
    return FilterDialog(sampling_frequency).run()


def _parse_float(text: str, label: str) -> float:
    """Parse a finite number, accepting a comma as the decimal separator."""
    try:
        value = float(text.strip().replace(",", "."))
    except ValueError:
        raise ValueError(f"{label} must be a number, got '{text}'") from None
    if not math.isfinite(value):
        raise ValueError(f"{label} must be a finite number, got '{text}'")
    return value


def _parse_int(text: str, label: str) -> int:
    try:
        return int(text.strip())
    except ValueError:
        raise ValueError(f"{label} must be a whole number, got '{text}'") from None