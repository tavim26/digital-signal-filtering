"""Application entry point.

Loads a signal from CSV, lets the user configure a filter in the GUI,
filters the signal, saves the result and plots it in the time and
frequency domains. Run with ``python -m signal_filtering`` or with the
``signal-filtering`` command installed by pip.
"""

from __future__ import annotations

import sys

from signal_filtering import config, gui, visualization
from signal_filtering.data_io import load_signal_from_csv, save_signal_to_csv
from signal_filtering.filters import apply_filter
from signal_filtering.signals import create_default_test_file


def main() -> int:
    """Run the application and return the process exit code."""
    input_path = config.DEFAULT_INPUT_FILE
    if not input_path.exists():
        print(f"Input file not found: {input_path}")
        print("Generating the default test signal...")
        create_default_test_file(input_path)

    try:
        signal = load_signal_from_csv(input_path)
    except (FileNotFoundError, ValueError) as err:
        print(f"Error: {err}", file=sys.stderr)
        return 1

    fs = signal.sampling_frequency
    print(
        f"Loaded {input_path.name}: {len(signal.values)} samples, "
        f"sampling frequency {fs:g} Hz (Nyquist {fs / 2:g} Hz)"
    )

    settings = gui.get_filter_settings(fs)
    if settings is None:
        print("Cancelled.")
        return 0

    # The GUI has already validated the settings, so this only fails for
    # problems that depend on the data itself (e.g. a signal too short).
    try:
        filtered = apply_filter(
            signal.values, settings.filter_type, settings.cutoff, fs, settings.order
        )
    except ValueError as err:
        print(f"Error: filtering failed: {err}", file=sys.stderr)
        return 1

    description = visualization.describe_filter(
        settings.filter_type, settings.cutoff, settings.order
    )
    print(f"Applied {description}")

    output_path = (
        config.DATA_PROCESSED_DIR / f"{input_path.stem}_{settings.filter_type}.csv"
    )
    try:
        save_signal_to_csv(output_path, signal.time, filtered)
    except OSError as err:
        print(f"Error: could not save {output_path}: {err}", file=sys.stderr)
        return 1
    print(f"Saved filtered signal to {output_path}")

    visualization.plot_time_domain(signal.time, signal.values, filtered, description)
    visualization.plot_frequency_domain(
        signal.values, filtered, fs, description, settings.cutoff
    )
    visualization.show_figures()
    return 0


if __name__ == "__main__":
    sys.exit(main())