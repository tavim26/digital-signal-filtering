"""Time- and frequency-domain plots comparing a signal before and after filtering."""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from scipy.signal import find_peaks

from signal_filtering import config
from signal_filtering.validation import Cutoff

# Spectral peaks smaller than this fraction of the largest one are not labelled.
PEAK_LABEL_THRESHOLD = 0.2
MAX_LABELLED_PEAKS = 5


def describe_filter(filter_type: str, cutoff: Cutoff, order: int) -> str:
    """Return a one-line description, e.g. 'Band-pass filter, 20-80 Hz, order 4'."""
    name = config.FILTER_TYPES[filter_type]
    if filter_type == "bandpass":
        low, high = cutoff
        band = f"{low:g}-{high:g} Hz"
    else:
        band = f"cutoff {cutoff:g} Hz"
    return f"{name} filter, {band}, order {order}"


def amplitude_spectrum(
    signal: np.ndarray, sampling_frequency: float
) -> tuple[np.ndarray, np.ndarray]:
    """Compute the single-sided amplitude spectrum of a real signal.

    The FFT output is scaled so that a sinusoid of amplitude A produces a
    peak of height A, and a constant offset C appears as C at 0 Hz. This
    makes the spectrum directly comparable with the time-domain signal.

    Parameters
    ----------
    signal : np.ndarray
        Real-valued input signal.
    sampling_frequency : float
        Sampling frequency, in Hz.

    Returns
    -------
    frequencies : np.ndarray
        Frequency of each bin, from 0 Hz up to the Nyquist frequency.
    amplitudes : np.ndarray
        Amplitude of each bin, in the units of the signal.
    """
    n = len(signal)
    # rfft returns only the non-negative frequencies of a real signal.
    amplitudes = np.abs(np.fft.rfft(signal)) / n
    # Each positive-frequency bin also carries the energy of its mirrored
    # negative-frequency twin, so it is doubled. The DC bin has no twin,
    # and neither does the Nyquist bin when n is even.
    amplitudes[1:] *= 2
    if n % 2 == 0:
        amplitudes[-1] /= 2
    frequencies = np.fft.rfftfreq(n, d=1 / sampling_frequency)
    return frequencies, amplitudes


def plot_time_domain(
    time: np.ndarray,
    original: np.ndarray,
    filtered: np.ndarray,
    description: str,
) -> Figure:
    """Plot the original and filtered signals over time.

    Three stacked panels share both axes, so amplitudes can be compared
    directly: the original signal, the filtered signal, and an overlay.

    Returns
    -------
    Figure
        The created figure; call ``show_figures`` to display it.
    """
    fig, (ax_original, ax_filtered, ax_overlay) = plt.subplots(
        3, 1, figsize=config.FIGURE_SIZE, dpi=config.DPI,
        sharex=True, sharey=True, layout="constrained",
    )
    _set_window_title(fig, "Time Domain")
    fig.suptitle(f"Time domain - {description}", fontsize=14, fontweight="bold")

    ax_original.plot(time, original, color=config.COLOR_ORIGINAL, linewidth=0.8)
    ax_original.set_title("Original signal")
    _add_statistics_box(ax_original, original)

    ax_filtered.plot(time, filtered, color=config.COLOR_FILTERED, linewidth=1.0)
    ax_filtered.set_title("Filtered signal")
    _add_statistics_box(ax_filtered, filtered)

    ax_overlay.plot(time, original, color=config.COLOR_ORIGINAL,
                    linewidth=0.8, alpha=0.5, label="Original")
    ax_overlay.plot(time, filtered, color=config.COLOR_FILTERED,
                    linewidth=1.2, label="Filtered")
    ax_overlay.set_title("Overlay")
    ax_overlay.legend(loc="upper right")
    ax_overlay.set_xlabel("Time (s)")
    ax_overlay.set_xlim(time[0], time[-1])

    for ax in (ax_original, ax_filtered, ax_overlay):
        ax.set_ylabel("Amplitude")
        _style_axes(ax)

    return fig


def plot_frequency_domain(
    original: np.ndarray,
    filtered: np.ndarray,
    sampling_frequency: float,
    description: str,
    cutoff: Cutoff | None = None,
) -> Figure:
    """Plot the amplitude spectra of the original and filtered signals.

    Three stacked panels share both axes: the original spectrum (with its
    dominant peaks labelled), the filtered spectrum, and an overlay. If
    ``cutoff`` is given, the cutoff frequencies are marked on every panel.

    Returns
    -------
    Figure
        The created figure; call ``show_figures`` to display it.
    """
    frequencies, original_spectrum = amplitude_spectrum(original, sampling_frequency)
    _, filtered_spectrum = amplitude_spectrum(filtered, sampling_frequency)

    fig, (ax_original, ax_filtered, ax_overlay) = plt.subplots(
        3, 1, figsize=config.FIGURE_SIZE, dpi=config.DPI,
        sharex=True, sharey=True, layout="constrained",
    )
    _set_window_title(fig, "Frequency Domain")
    fig.suptitle(f"Frequency domain - {description}", fontsize=14, fontweight="bold")

    ax_original.plot(frequencies, original_spectrum,
                     color=config.COLOR_ORIGINAL, linewidth=1.0)
    ax_original.set_title("Original spectrum")
    _label_peaks(ax_original, frequencies, original_spectrum)

    ax_filtered.plot(frequencies, filtered_spectrum,
                     color=config.COLOR_FILTERED, linewidth=1.0)
    ax_filtered.set_title("Filtered spectrum")

    ax_overlay.plot(frequencies, original_spectrum, color=config.COLOR_ORIGINAL,
                    linewidth=1.0, alpha=0.5, label="Original")
    ax_overlay.plot(frequencies, filtered_spectrum, color=config.COLOR_FILTERED,
                    linewidth=1.2, label="Filtered")
    ax_overlay.set_title("Overlay")
    ax_overlay.set_xlabel("Frequency (Hz)")

    nyquist = sampling_frequency / 2
    # A small left margin keeps the 0 Hz (DC) bin visible instead of hidden
    # behind the y-axis.
    ax_overlay.set_xlim(-0.01 * nyquist, nyquist)

    for ax in (ax_original, ax_filtered, ax_overlay):
        if cutoff is not None:
            _mark_cutoffs(ax, cutoff)
        ax.set_ylabel("Amplitude")
        _style_axes(ax)
    # Created after the cutoff lines so the legend includes them.
    ax_overlay.legend(loc="upper right")

    return fig


def show_figures() -> None:
    """Display all open figures, blocking until the user closes them."""
    plt.show()


def _set_window_title(fig: Figure, title: str) -> None:
    # Non-interactive backends (e.g. when saving to file) have no window.
    manager = fig.canvas.manager
    if manager is not None:
        manager.set_window_title(title)


def _add_statistics_box(ax: Axes, signal: np.ndarray) -> None:
    """Show the mean (DC level) and standard deviation in a corner of the axes."""
    ax.text(
        0.01, 0.95,
        f"Mean: {np.mean(signal):.4f}\nStd: {np.std(signal):.4f}",
        transform=ax.transAxes, fontsize=9, verticalalignment="top",
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.8),
    )


def _label_peaks(ax: Axes, frequencies: np.ndarray, spectrum: np.ndarray) -> None:
    """Annotate the strongest local maxima of a spectrum with their frequency."""
    threshold = PEAK_LABEL_THRESHOLD * spectrum.max()
    peaks, properties = find_peaks(spectrum, height=threshold)
    strongest = peaks[np.argsort(properties["peak_heights"])[::-1][:MAX_LABELLED_PEAKS]]
    for index in strongest:
        ax.annotate(
            f"{frequencies[index]:g} Hz",
            xy=(frequencies[index], spectrum[index]),
            xytext=(0, 4), textcoords="offset points",
            ha="center", va="bottom", fontsize=9,
        )


def _mark_cutoffs(ax: Axes, cutoff: Cutoff) -> None:
    """Draw dashed vertical lines at the cutoff frequency or frequencies."""
    cutoffs = cutoff if isinstance(cutoff, (tuple, list)) else (cutoff,)
    for i, frequency in enumerate(cutoffs):
        ax.axvline(frequency, color="gray", linestyle="--", linewidth=1,
                   label="Cutoff" if i == 0 else None)


def _style_axes(ax: Axes) -> None:
    ax.grid(True, alpha=0.3, linestyle="--", linewidth=0.5)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)