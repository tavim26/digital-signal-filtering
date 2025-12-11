"""
Module pentru vizualizarea semnalelor si rezultatelor filtrarii
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal as sig
import sys
import os

# Import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config


def plot_signals(time, original_signal, filtered_signal, title="Comparatie Semnal Original vs Filtrat"):
    """
    Afiseaza comparatie intre semnalul original si cel filtrat

    Parameters:
    -----------
    time : numpy.ndarray
        Vector timp
    original_signal : numpy.ndarray
        Semnalul original
    filtered_signal : numpy.ndarray
        Semnalul filtrat
    title : str
        Titlul graficului
    """
    plt.figure(figsize=config.FIGURE_SIZE, dpi=config.DPI)

    plt.plot(time, original_signal, label='Semnal Original',
             color=config.COLOR_ORIGINAL, alpha=0.7, linewidth=1)
    plt.plot(time, filtered_signal, label='Semnal Filtrat',
             color=config.COLOR_FILTERED, linewidth=2)

    plt.xlabel('Timp (s)', fontsize=12)
    plt.ylabel('Amplitudine', fontsize=12)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.legend(loc='best', fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def plot_frequency_spectrum(time, original_signal, filtered_signal, sampling_freq,
                            title="Spectru de Frecventa"):
    """
    Afiseaza spectrul de frecventa pentru ambele semnale

    Parameters:
    -----------
    time : numpy.ndarray
        Vector timp
    original_signal : numpy.ndarray
        Semnalul original
    filtered_signal : numpy.ndarray
        Semnalul filtrat
    sampling_freq : float
        Frecventa de esantionare
    title : str
        Titlul graficului
    """
    # Calculeaza FFT pentru semnalul original
    n = len(original_signal)
    freq = np.fft.fftfreq(n, d=1 / sampling_freq)
    fft_original = np.fft.fft(original_signal)
    fft_filtered = np.fft.fft(filtered_signal)

    # Pastreaza doar frecventele pozitive
    positive_freq_idx = freq > 0
    freq = freq[positive_freq_idx]
    fft_original = np.abs(fft_original[positive_freq_idx])
    fft_filtered = np.abs(fft_filtered[positive_freq_idx])

    # Plotare
    plt.figure(figsize=config.FIGURE_SIZE, dpi=config.DPI)

    plt.subplot(2, 1, 1)
    plt.plot(freq, fft_original, color=config.COLOR_ORIGINAL, linewidth=1.5)
    plt.xlabel('Frecventa (Hz)', fontsize=11)
    plt.ylabel('Magnitudine', fontsize=11)
    plt.title('Spectru Original', fontsize=12, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.xlim(0, sampling_freq / 2)

    plt.subplot(2, 1, 2)
    plt.plot(freq, fft_filtered, color=config.COLOR_FILTERED, linewidth=1.5)
    plt.xlabel('Frecventa (Hz)', fontsize=11)
    plt.ylabel('Magnitudine', fontsize=11)
    plt.title('Spectru Filtrat', fontsize=12, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.xlim(0, sampling_freq / 2)

    plt.suptitle(title, fontsize=14, fontweight='bold', y=1.00)
    plt.tight_layout()
    plt.show()


def plot_filter_response(frequencies, response, filter_type, cutoff_info):
    """
    Afiseaza raspunsul in frecventa al filtrului

    Parameters:
    -----------
    frequencies : numpy.ndarray
        Vector de frecvente
    response : numpy.ndarray
        Raspunsul in frecventa
    filter_type : str
        Tipul filtrului
    cutoff_info : str
        Informatii despre frecventele de taiere
    """
    plt.figure(figsize=(10, 6), dpi=config.DPI)

    # Magnitudine in dB
    plt.subplot(2, 1, 1)
    plt.plot(frequencies, 20 * np.log10(np.abs(response)),
             color=config.COLOR_SPECTRUM, linewidth=2)
    plt.xlabel('Frecventa (Hz)', fontsize=11)
    plt.ylabel('Magnitudine (dB)', fontsize=11)
    plt.title(f'Raspuns in Frecventa - Filtru {filter_type}\n{cutoff_info}',
              fontsize=12, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.ylim(-80, 5)

    # Magnitudine liniara
    plt.subplot(2, 1, 2)
    plt.plot(frequencies, np.abs(response),
             color=config.COLOR_SPECTRUM, linewidth=2)
    plt.xlabel('Frecventa (Hz)', fontsize=11)
    plt.ylabel('Magnitudine', fontsize=11)
    plt.title('Raspuns Liniar', fontsize=12, fontweight='bold')
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()


def plot_all_analysis(time, original_signal, filtered_signal, sampling_freq,
                      filter_type, cutoff_info):
    """
    Afiseaza analiza completa: semnal temporal + spectru frecventa

    Parameters:
    -----------
    time : numpy.ndarray
        Vector timp
    original_signal : numpy.ndarray
        Semnalul original
    filtered_signal : numpy.ndarray
        Semnalul filtrat
    sampling_freq : float
        Frecventa de esantionare
    filter_type : str
        Tipul filtrului aplicat
    cutoff_info : str
        Informatii despre frecventele de taiere
    """
    fig = plt.figure(figsize=(16, 10), dpi=config.DPI)

    # Semnale temporale
    plt.subplot(2, 2, 1)
    plt.plot(time, original_signal, label='Original',
             color=config.COLOR_ORIGINAL, alpha=0.7, linewidth=1)
    plt.xlabel('Timp (s)', fontsize=10)
    plt.ylabel('Amplitudine', fontsize=10)
    plt.title('Semnal Original', fontsize=11, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.legend()

    plt.subplot(2, 2, 2)
    plt.plot(time, filtered_signal, label='Filtrat',
             color=config.COLOR_FILTERED, linewidth=1.5)
    plt.xlabel('Timp (s)', fontsize=10)
    plt.ylabel('Amplitudine', fontsize=10)
    plt.title('Semnal Filtrat', fontsize=11, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.legend()

    # Spectru de frecventa
    n = len(original_signal)
    freq = np.fft.fftfreq(n, d=1 / sampling_freq)
    fft_original = np.fft.fft(original_signal)
    fft_filtered = np.fft.fft(filtered_signal)

    positive_freq_idx = freq > 0
    freq = freq[positive_freq_idx]
    fft_original = np.abs(fft_original[positive_freq_idx])
    fft_filtered = np.abs(fft_filtered[positive_freq_idx])

    plt.subplot(2, 2, 3)
    plt.plot(freq, fft_original, color=config.COLOR_ORIGINAL, linewidth=1.5)
    plt.xlabel('Frecventa (Hz)', fontsize=10)
    plt.ylabel('Magnitudine', fontsize=10)
    plt.title('Spectru Original', fontsize=11, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.xlim(0, sampling_freq / 2)

    plt.subplot(2, 2, 4)
    plt.plot(freq, fft_filtered, color=config.COLOR_FILTERED, linewidth=1.5)
    plt.xlabel('Frecventa (Hz)', fontsize=10)
    plt.ylabel('Magnitudine', fontsize=10)
    plt.title('Spectru Filtrat', fontsize=11, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.xlim(0, sampling_freq / 2)

    plt.suptitle(f'Analiza Completa - Filtru {filter_type}\n{cutoff_info}',
                 fontsize=13, fontweight='bold')
    plt.tight_layout()
    plt.show()