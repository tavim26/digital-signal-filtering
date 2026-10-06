"""Zero-phase Butterworth IIR filters: low-pass, high-pass and band-pass."""

from __future__ import annotations

import numpy as np
from scipy.signal import butter, sosfiltfilt

from signal_filtering import config
from signal_filtering.validation import Cutoff, validate_filter_parameters


def design_butterworth(
    filter_type: str,
    cutoff: Cutoff,
    sampling_frequency: float,
    order: int = config.DEFAULT_FILTER_ORDER,
) -> np.ndarray:
    """Design a digital Butterworth filter in second-order sections form.

    The Butterworth response is maximally flat in the passband (no ripple),
    at the cost of a wider transition band than Chebyshev or elliptic
    designs of the same order.

    The filter is returned as second-order sections (SOS) rather than as
    numerator/denominator polynomials (b, a). The polynomial form becomes
    numerically unstable at high orders or low normalized cutoffs, because
    small rounding errors in the coefficients move the poles significantly.
    A cascade of second-order sections avoids this.

    Parameters
    ----------
    filter_type : str
        "lowpass", "highpass" or "bandpass".
    cutoff : float or tuple of float
        Cutoff frequency in Hz, or a ``(low, high)`` pair for band-pass.
    sampling_frequency : float
        Sampling frequency, in Hz.
    order : int
        Filter order. A band-pass filter of order N has 2N poles.

    Returns
    -------
    np.ndarray
        Array of shape ``(n_sections, 6)``, as expected by ``sosfiltfilt``.

    Raises
    ------
    ValueError
        If the parameters fail validation.
    """
    validate_filter_parameters(filter_type, cutoff, sampling_frequency, order)
    return butter(
        order, cutoff, btype=filter_type, fs=sampling_frequency, output="sos"
    )


def apply_filter(
    data: np.ndarray,
    filter_type: str,
    cutoff: Cutoff,
    sampling_frequency: float,
    order: int = config.DEFAULT_FILTER_ORDER,
) -> np.ndarray:
    """Filter a signal with a zero-phase Butterworth filter.

    The filter is run forwards and then backwards over the signal
    (``sosfiltfilt``). The phase shifts of the two passes cancel, so the
    output has no time delay relative to the input, which keeps features
    such as peaks aligned with the original signal.

    Because the magnitude response is applied twice, it is effectively
    squared: the attenuation in dB doubles, the roll-off is as steep as
    a filter of twice the order, and the gain at the cutoff frequency is
    -6 dB instead of the usual -3 dB.

    Parameters
    ----------
    data : np.ndarray
        Input signal.
    filter_type : str
        "lowpass", "highpass" or "bandpass".
    cutoff : float or tuple of float
        Cutoff frequency in Hz, or a ``(low, high)`` pair for band-pass.
    sampling_frequency : float
        Sampling frequency, in Hz.
    order : int
        Filter order of each pass.

    Returns
    -------
    np.ndarray
        The filtered signal, with the same length as ``data``.

    Raises
    ------
    ValueError
        If the parameters fail validation, or if the signal is too short
        for the edge padding that ``sosfiltfilt`` applies.
    """
    sos = design_butterworth(filter_type, cutoff, sampling_frequency, order)
    return sosfiltfilt(sos, data)