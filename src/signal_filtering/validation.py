"""Validation of filter parameters, shared by the filters and the GUI."""

from __future__ import annotations

from signal_filtering import config

# A single cutoff frequency (low-pass, high-pass) or a (low, high) pair
# (band-pass), in Hz.
Cutoff = float | tuple[float, float]


def validate_filter_parameters(
    filter_type: str,
    cutoff: Cutoff,
    sampling_frequency: float,
    order: int,
) -> None:
    """Check that the filter parameters describe a realizable filter.

    Every cutoff must lie strictly between 0 Hz and the Nyquist frequency
    (half the sampling frequency): the digital frequency axis ends there,
    so a cutoff at or above it has no meaning.

    Parameters
    ----------
    filter_type : str
        One of the keys of ``config.FILTER_TYPES``.
    cutoff : float or tuple of float
        Cutoff frequency in Hz, or a ``(low, high)`` pair for band-pass.
    sampling_frequency : float
        Sampling frequency of the signal, in Hz.
    order : int
        Filter order.

    Raises
    ------
    ValueError
        With a user-readable message describing the first problem found.
    """
    if filter_type not in config.FILTER_TYPES:
        raise ValueError(
            f"Unknown filter type {filter_type!r}; "
            f"expected one of: {', '.join(config.FILTER_TYPES)}"
        )

    if isinstance(order, bool) or not isinstance(order, int):
        raise ValueError(f"Filter order must be an integer, got {order!r}")
    if not config.MIN_FILTER_ORDER <= order <= config.MAX_FILTER_ORDER:
        raise ValueError(
            f"Filter order must be between {config.MIN_FILTER_ORDER} "
            f"and {config.MAX_FILTER_ORDER}, got {order}"
        )

    if sampling_frequency <= 0:
        raise ValueError("Sampling frequency must be positive")
    nyquist = sampling_frequency / 2

    if filter_type == "bandpass":
        try:
            low, high = cutoff
        except (TypeError, ValueError):
            raise ValueError(
                "Band-pass filter needs a (low, high) pair of cutoff frequencies"
            ) from None
        if low <= 0:
            raise ValueError(f"Lower cutoff ({low} Hz) must be greater than 0 Hz")
        if low >= high:
            raise ValueError(
                f"Lower cutoff ({low} Hz) must be less than "
                f"upper cutoff ({high} Hz)"
            )
        if high >= nyquist:
            raise ValueError(
                f"Upper cutoff ({high} Hz) must be less than "
                f"the Nyquist frequency ({nyquist:g} Hz)"
            )
    else:
        if isinstance(cutoff, (tuple, list)):
            raise ValueError(
                f"{config.FILTER_TYPES[filter_type]} filter needs a single "
                "cutoff frequency"
            )
        if not 0 < cutoff < nyquist:
            raise ValueError(
                f"Cutoff ({cutoff} Hz) must be between 0 Hz and "
                f"the Nyquist frequency ({nyquist:g} Hz)"
            )