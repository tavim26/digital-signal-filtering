"""Project-wide configuration: paths, default parameters and plot styling."""

from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
# This file lives in <repo>/src/signal_filtering/, so the repository root
# is two levels above its parent directory.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_RAW_DIR = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
DEFAULT_INPUT_FILE = DATA_RAW_DIR / "test_signal.csv"

# ---------------------------------------------------------------------------
# Test signal generation
# ---------------------------------------------------------------------------
DEFAULT_SAMPLING_FREQUENCY = 1000.0  # Hz
DEFAULT_DURATION = 2.0               # seconds

# ---------------------------------------------------------------------------
# Filter defaults
# ---------------------------------------------------------------------------
DEFAULT_FILTER_ORDER = 4
MIN_FILTER_ORDER = 1
MAX_FILTER_ORDER = 10

# Supported filter types (keys are the scipy names) and their display names.
FILTER_TYPES = {
    "lowpass": "Low-pass",
    "highpass": "High-pass",
    "bandpass": "Band-pass",
}

# Default cutoffs, expressed as fractions of the Nyquist frequency so they
# remain valid for any sampling rate loaded from a file.
DEFAULT_LOWPASS_CUTOFF_RATIO = 0.10
DEFAULT_HIGHPASS_CUTOFF_RATIO = 0.02
DEFAULT_BANDPASS_LOW_RATIO = 0.04
DEFAULT_BANDPASS_HIGH_RATIO = 0.16

# ---------------------------------------------------------------------------
# Plot styling
# ---------------------------------------------------------------------------
FIGURE_SIZE = (14, 9)  # inches
DPI = 100

COLOR_ORIGINAL = "#2E86AB"
COLOR_FILTERED = "#A23B72"