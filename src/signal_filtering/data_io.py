"""Reading and writing time-domain signals stored as CSV files."""

from __future__ import annotations

from pathlib import Path
from typing import NamedTuple

import numpy as np
import pandas as pd

# Column names used when writing signals to disk.
TIME_COLUMN_NAME = "time"
SIGNAL_COLUMN_NAME = "signal"

# Maximum relative deviation of any sampling interval from the mean interval
# before the signal is rejected as non-uniformly sampled. IIR filters assume
# a constant sampling rate, so irregular timestamps would give wrong results.
UNIFORM_SAMPLING_TOLERANCE = 0.01


class SignalData(NamedTuple):
    """A uniformly sampled signal loaded from disk."""

    time: np.ndarray
    values: np.ndarray
    sampling_frequency: float


def load_signal_from_csv(
    filepath: str | Path,
    time_column: int | str = 0,
    signal_column: int | str = 1,
    delimiter: str = ",",
) -> SignalData:
    """Load a uniformly sampled signal from a CSV file.

    The sampling frequency is derived from the time column.

    Parameters
    ----------
    filepath : str or Path
        Path to the CSV file. The first row must be a header.
    time_column : int or str, default 0
        Index or name of the column holding the timestamps, in seconds.
    signal_column : int or str, default 1
        Index or name of the column holding the signal values.
    delimiter : str, default ","
        Field separator used in the file.

    Returns
    -------
    SignalData
        Timestamps, signal values and the sampling frequency in Hz.

    Raises
    ------
    FileNotFoundError
        If the file does not exist.
    ValueError
        If the file is not a CSV, cannot be parsed, has missing or
        non-numeric values, has fewer than two samples, or is not
        uniformly sampled.
    """
    path = Path(filepath)
    if not path.is_file():
        raise FileNotFoundError(f"File not found: {path}")
    if path.suffix.lower() != ".csv":
        raise ValueError(f"Expected a .csv file, got '{path.suffix}'")

    try:
        df = pd.read_csv(path, delimiter=delimiter)
    except (pd.errors.EmptyDataError, pd.errors.ParserError) as err:
        raise ValueError(f"Could not parse CSV file '{path.name}': {err}") from err

    time = _extract_numeric_column(df, time_column, "time")
    values = _extract_numeric_column(df, signal_column, "signal")

    if len(time) < 2:
        raise ValueError(f"At least 2 samples are required, found {len(time)}")

    sampling_frequency = _estimate_sampling_frequency(time)
    return SignalData(time, values, sampling_frequency)


def save_signal_to_csv(
    filepath: str | Path,
    time: np.ndarray,
    values: np.ndarray,
) -> Path:
    """Write a signal to a CSV file with 'time' and 'signal' columns.

    Missing parent directories are created automatically.

    Parameters
    ----------
    filepath : str or Path
        Destination file.
    time : np.ndarray
        Timestamps, in seconds.
    values : np.ndarray
        Signal values; must have the same length as ``time``.

    Returns
    -------
    Path
        The path of the written file.

    Raises
    ------
    ValueError
        If ``time`` and ``values`` have different lengths.
    """
    if len(time) != len(values):
        raise ValueError(
            f"Length mismatch: {len(time)} timestamps vs {len(values)} values"
        )

    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame({TIME_COLUMN_NAME: time, SIGNAL_COLUMN_NAME: values}).to_csv(
        path, index=False
    )
    return path


def _extract_numeric_column(
    df: pd.DataFrame, column: int | str, label: str
) -> np.ndarray:
    """Return a column as a float array, rejecting missing or non-numeric data."""
    try:
        series = df.iloc[:, column] if isinstance(column, int) else df[column]
    except (IndexError, KeyError) as err:
        raise ValueError(
            f"{label.capitalize()} column {column!r} not found; "
            f"available columns: {list(df.columns)}"
        ) from err

    values = pd.to_numeric(series, errors="coerce").to_numpy(dtype=float)

    invalid_rows = np.flatnonzero(np.isnan(values))
    if invalid_rows.size:
        # +2 converts a 0-based data row index into a 1-based file line
        # number, accounting for the header line.
        raise ValueError(
            f"{label.capitalize()} column contains {invalid_rows.size} missing "
            f"or non-numeric value(s), first at line {invalid_rows[0] + 2}"
        )
    return values


def _estimate_sampling_frequency(time: np.ndarray) -> float:
    """Derive the sampling frequency from timestamps, checking uniformity."""
    intervals = np.diff(time)
    if np.any(intervals <= 0):
        raise ValueError("Time values must be strictly increasing")

    mean_interval = intervals.mean()
    max_deviation = np.max(np.abs(intervals - mean_interval)) / mean_interval
    if max_deviation > UNIFORM_SAMPLING_TOLERANCE:
        raise ValueError(
            "Signal is not uniformly sampled: sampling intervals deviate by up "
            f"to {max_deviation:.1%} from the mean"
        )
    return 1.0 / mean_interval