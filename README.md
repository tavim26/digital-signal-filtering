# Digital Signal Filtering

A Python desktop application that applies Butterworth low-pass, high-pass and band-pass filters to signals loaded from CSV files, and compares the signal before and after filtering in the time and frequency domains.

## Features

- **Three filter types:** low-pass, high-pass and band-pass, with configurable order and cutoff frequencies
- **Zero-phase filtering:** the output is not delayed relative to the input
- **Input validation** in the GUI, including the Nyquist limit derived from the loaded file
- **Automatic sampling rate detection** from the time column, with checks for missing values and non-uniform sampling
- **Time-domain and frequency-domain plots** comparing the original and filtered signals
- **Reproducible test signal** generated automatically if no input file is present


## How It Works

1. **Load:** the CSV file is read and the sampling frequency is computed from the timestamps.
2. **Configure:** a Tkinter dialog collects the filter type, order and cutoff frequencies, and validates them before closing.
3. **Filter:** a Butterworth filter is designed with SciPy and applied to the signal.
4. **Save and plot:** the filtered signal is written to `data/processed/` and the results are plotted with Matplotlib.

A few implementation details:

- **Second-order sections.** Filters are designed in second-order sections (SOS) form rather than as transfer-function coefficients `(b, a)`. SOS remains numerically stable at high orders and low cutoff frequencies.
- **Forward-backward filtering.** `sosfiltfilt` runs the filter forwards and then backwards. The phase shifts cancel out, so there is no delay, but the magnitude response is squared: the gain at the cutoff frequency is −6 dB instead of −3 dB, and the roll-off is twice as steep.
- **Scaled spectrum.** The amplitude spectrum is scaled so that a sinusoid of amplitude *A* appears as a peak of height *A*, which makes it directly comparable with the time-domain signal.

## Requirements

- Python 3.10 or newer
- Tkinter. It is included with Python on Windows and macOS (python.org installer). On Debian/Ubuntu-based Linux, install it with:

```bash
  sudo apt install python3-tk
```

## Installation

```bash
git clone https://github.com/tavim26/digital-signal-filtering.git
cd digital-signal-filtering

python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

pip install -e .
```

## Usage

```bash
python -m signal_filtering
```

Choose a filter in the dialog and click **Apply Filter** (or press Enter). The filtered signal is saved to `data/processed/<input>_<filter>.csv`, and two plot windows open.

### Input format

The application reads `data/raw/test_signal.csv`. To filter your own data, replace this file, or change `DEFAULT_INPUT_FILE` in `src/signal_filtering/config.py`.

The file must have a header row and two numeric columns:

```csv
time,signal
0.000,0.512
0.001,1.203
...
```

- The **first column** holds the timestamps, in seconds.
- The **second column** holds the signal values.
- Samples must be **uniformly spaced** in time.

### Test signal

If the input file is missing, a test signal is generated automatically. You can also regenerate it with:

```bash
python -m signal_filtering.signals
```

It lasts 2 seconds at 1000 Hz and is built so that each filter has a clearly visible effect with its default settings:

| Component | Low-pass 50 Hz | High-pass 10 Hz | Band-pass 20–80 Hz |
|---|---|---|---|
| DC offset (0.5) | kept | removed | removed |
| 2 Hz sine (amplitude 1.0) | kept | removed | removed |
| 40 Hz sine (amplitude 0.8) | kept | kept | kept |
| 200 Hz sine (amplitude 0.5) | removed | kept | removed |
| White noise (σ = 0.2) | reduced | partly reduced | reduced |

## Project Structure

```
digital-signal-filtering/
├── data/
│   ├── raw/                  # input signals
│   └── processed/            # filtered output (generated)
├── docs/images/              # screenshots used in this README
├── src/signal_filtering/
│   ├── __main__.py           # application entry point
│   ├── config.py             # paths, defaults and plot settings
│   ├── data_io.py            # CSV loading, validation and saving
│   ├── filters.py            # Butterworth filter design and application
│   ├── gui.py                # Tkinter configuration dialog
│   ├── signals.py            # test signal generator
│   ├── validation.py         # filter parameter validation
│   └── visualization.py      # time- and frequency-domain plots
└── pyproject.toml
```

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.