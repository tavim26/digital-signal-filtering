"""Digital signal filtering: Butterworth filters applied to CSV signals."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("signal-filtering")
except PackageNotFoundError:  # running from source without installation
    __version__ = "unknown"