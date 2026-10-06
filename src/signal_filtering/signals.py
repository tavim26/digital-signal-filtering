"""Synthetic test signals for demonstrating the filters."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np

from signal_filtering import config
from signal_filtering.data_io import SignalData, save_signal_to_csv


@dataclass(frozen=True)
class SineComponent:
    """A single sinusoid: amplitude * sin(2*pi*frequency*t + phase)."""

    frequency: float  # Hz
    amplitude: float
    phase: float = 0.0  # radians


# Chosen so each default filter in config.py has a clearly visible effect:
# the 2 Hz component and the DC offset are removed by the high-pass filter,
# the 200 Hz component by the low-pass filter, and the band-pass filter
# isolates the 40 Hz component.
DEFAULT_COMPONENTS: tuple[SineComponent, ...] = (
    SineComponent(frequency=2.0, amplitude=1.0),
    SineComponent(frequency=40.0, amplitude=0.8),
    SineComponent(frequency=200.0, amplitude=0.5),
)
DEFAULT_DC_OFFSET = 0.5
DEFAULT_NOISE_STD = 0.2


def generate_test_signal(
    sampling_frequency: float = config.DEFAULT_SAMPLING_FREQUENCY,
    duration: float = config.DEFAULT_DURATION,
    components: tuple[SineComponent, ...] = DEFAULT_COMPONENTS,
    dc_offset: float = DEFAULT_DC_OFFSET,
    noise_std: float = DEFAULT_NOISE_STD,
    seed: int | None = 0,
) -> SignalData:
    """Generate a sum of sinusoids with a DC offset and Gaussian white noise.

    Parameters
    ----------
    sampling_frequency : float
        Sampling frequency, in Hz.
    duration : float
        Signal length, in seconds.
    components : tuple of SineComponent
        Sinusoids to add together.
    dc_offset : float
        Constant added to every sample.
    noise_std : float
        Standard deviation of the additive white noise; 0 disables noise.
    seed : int or None, default 0
        Random seed for the noise. A fixed seed makes the output
        reproducible; None gives different noise on every call.

    Returns
    -------
    SignalData
        Timestamps, signal values and the sampling frequency.

    Raises
    ------
    ValueError
        If any parameter is out of range, or if a component lies at or
        above the Nyquist frequency (it would alias to a lower frequency).
    """
    if sampling_frequency <= 0:
        raise ValueError("Sampling frequency must be positive")
    if duration <= 0:
        raise ValueError("Duration must be positive")
    if noise_std < 0:
        raise ValueError("Noise standard deviation cannot be negative")

    nyquist = sampling_frequency / 2
    for component in components:
        if not 0 < component.frequency < nyquist:
            raise ValueError(
                f"Component frequency {component.frequency} Hz must lie "
                f"between 0 and the Nyquist frequency ({nyquist} Hz)"
            )

    num_samples = round(duration * sampling_frequency)
    time = np.arange(num_samples) / sampling_frequency

    values = np.full(num_samples, dc_offset, dtype=float)
    for component in components:
        values += component.amplitude * np.sin(
            2 * np.pi * component.frequency * time + component.phase
        )

    if noise_std > 0:
        rng = np.random.default_rng(seed)
        values += rng.normal(0.0, noise_std, num_samples)

    return SignalData(time, values, sampling_frequency)


def create_default_test_file(
    filepath: str | Path = config.DEFAULT_INPUT_FILE,
) -> Path:
    """Generate the default test signal and write it to a CSV file.

    Returns
    -------
    Path
        The path of the written file.
    """
    signal = generate_test_signal()
    return save_signal_to_csv(filepath, signal.time, signal.values)


if __name__ == "__main__":
    output_path = create_default_test_file()
    print(f"Test signal written to {output_path}")