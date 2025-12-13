"""
Module pentru vizualizarea semnalelor si rezultatelor filtrarii
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal as sig
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config


def plot_time_domain_comparison(time, original_signal, filtered_signal, filter_type, cutoff_info):
    """
    Fereastra 1: Comparatie semnale in domeniul timp

    Parameters:
    time : Vector timp
    original_signal : Semnalul original
    filtered_signal : Semnalul filtrat
    filter_type : Tipul filtrului
    cutoff_info : Informatii despre frecventele de taiere
    """
    filter_names = {
        'lowpass': 'Trece-Jos',
        'highpass': 'Trece-Sus',
        'bandpass': 'Trece-Banda'
    }
    filter_name_ro = filter_names.get(filter_type.lower(), filter_type)

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(16, 10))
    fig.canvas.manager.set_window_title('Analiza Temporala')

    # Titlu general
    fig.suptitle(f'Analiza Domeniu Timp - Filtru {filter_name_ro}\n{cutoff_info}',
                 fontsize=15, fontweight='bold')

    # Grafic 1: Semnal Original
    ax1.plot(time, original_signal, color=config.COLOR_ORIGINAL, linewidth=1.5, alpha=0.8)
    ax1.set_xlabel('Timp (secunde)', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Amplitudine', fontsize=11, fontweight='bold')
    ax1.set_title('Semnal Original (inainte de filtrare)\nContine toate componentele de frecventa',
                  fontsize=12, fontweight='bold', pad=10)
    ax1.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
    ax1.set_xlim(time[0], time[-1])

    # Statistici semnal original
    mean_orig = np.mean(original_signal)
    std_orig = np.std(original_signal)
    ax1.text(0.02, 0.95, f'Media: {mean_orig:.4f}\nDeviatia std: {std_orig:.4f}',
             transform=ax1.transAxes, fontsize=10, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    # Grafic 2: Semnal Filtrat
    ax2.plot(time, filtered_signal, color=config.COLOR_FILTERED, linewidth=2)
    ax2.set_xlabel('Timp (secunde)', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Amplitudine', fontsize=11, fontweight='bold')
    ax2.set_title('Semnal Filtrat (dupa aplicarea filtrului)\nComponentele nedorite au fost eliminate',
                  fontsize=12, fontweight='bold', pad=10)
    ax2.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
    ax2.set_xlim(time[0], time[-1])

    # Statistici semnal filtrat
    mean_filt = np.mean(filtered_signal)
    std_filt = np.std(filtered_signal)
    ax2.text(0.02, 0.95, f'Media: {mean_filt:.4f}\nDeviatia std: {std_filt:.4f}',
             transform=ax2.transAxes, fontsize=10, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))

    # Grafic 3: Comparatie suprapusa
    ax3.plot(time, original_signal, label='Semnal Original',
             color=config.COLOR_ORIGINAL, linewidth=1.2, alpha=0.6)
    ax3.plot(time, filtered_signal, label='Semnal Filtrat',
             color=config.COLOR_FILTERED, linewidth=2.5)
    ax3.set_xlabel('Timp (secunde)', fontsize=11, fontweight='bold')
    ax3.set_ylabel('Amplitudine', fontsize=11, fontweight='bold')
    ax3.set_title('Comparatie Directa: Original (transparent) vs Filtrat (solid)\nObserva diferentele de amplitudine si netezire',
                  fontsize=12, fontweight='bold', pad=10)
    ax3.legend(loc='upper right', fontsize=11, framealpha=0.9)
    ax3.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
    ax3.set_xlim(time[0], time[-1])

    # Stilizare
    for ax in [ax1, ax2, ax3]:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_linewidth(1.5)
        ax.spines['bottom'].set_linewidth(1.5)

    plt.tight_layout()
    plt.show(block=False)



def plot_frequency_domain_comparison(time, original_signal, filtered_signal, sampling_freq,
                                     filter_type, cutoff_info):
    """
    Fereastra 2: Analiza spectru de frecventa (FFT)

    Parameters:
    -----------
    time : Vector timp
    original_signal : Semnalul original
    filtered_signal : Semnalul filtrat
    sampling_freq : Frecventa de esantionare
    filter_type : Tipul filtrului
    cutoff_info : Informatii despre frecventele de taiere
    """
    filter_names = {
        'lowpass': 'Trece-Jos',
        'highpass': 'Trece-Sus',
        'bandpass': 'Trece-Banda'
    }
    filter_name_ro = filter_names.get(filter_type.lower(), filter_type)

    # Calcul FFT
    n = len(original_signal)
    freq = np.fft.fftfreq(n, d=1/sampling_freq)
    fft_original = np.fft.fft(original_signal)
    fft_filtered = np.fft.fft(filtered_signal)

    # Pastreaza doar frecventele pozitive
    positive_freq_idx = freq > 0
    freq_pos = freq[positive_freq_idx]
    fft_mag_original = np.abs(fft_original[positive_freq_idx])
    fft_mag_filtered = np.abs(fft_filtered[positive_freq_idx])

    # Creaza figura
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(16, 10))
    fig.canvas.manager.set_window_title('Analiza Spectrala (FFT)')

    fig.suptitle(f'Analiza Spectru de Frecventa (FFT) - Filtru {filter_name_ro}\n{cutoff_info}',
                 fontsize=15, fontweight='bold')

    # Grafic 1: Spectru Original
    ax1.plot(freq_pos, fft_mag_original, color=config.COLOR_ORIGINAL, linewidth=1.5)
    ax1.set_xlabel('Frecventa (Hz)', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Magnitudine (Amplitudine FFT)', fontsize=11, fontweight='bold')
    ax1.set_title('Spectru de Frecventa Original\nArata toate componentele de frecventa prezente in semnal',
                  fontsize=12, fontweight='bold', pad=10)
    ax1.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
    ax1.set_xlim(0, sampling_freq / 2)

    # Gaseste frecventele dominante in spectrul original
    dominant_freqs_idx = np.argsort(fft_mag_original)[-3:]  # Top 3 frecvente
    for idx in dominant_freqs_idx:
        if fft_mag_original[idx] > np.max(fft_mag_original) * 0.3:  # Doar daca semnificative
            ax1.axvline(x=freq_pos[idx], color='red', linestyle=':', alpha=0.5, linewidth=1)
            ax1.text(freq_pos[idx], fft_mag_original[idx], f'{freq_pos[idx]:.1f} Hz',
                    fontsize=9, rotation=90, verticalalignment='bottom')

    # Grafic 2: Spectru Filtrat
    ax2.plot(freq_pos, fft_mag_filtered, color=config.COLOR_FILTERED, linewidth=1.5)
    ax2.set_xlabel('Frecventa (Hz)', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Magnitudine (Amplitudine FFT)', fontsize=11, fontweight='bold')
    ax2.set_title('Spectru de Frecventa Filtrat\nComponentele nedorite au fost atenuate/eliminate',
                  fontsize=12, fontweight='bold', pad=10)
    ax2.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
    ax2.set_xlim(0, sampling_freq / 2)

    # Grafic 3: Comparatie suprapusa
    ax3.plot(freq_pos, fft_mag_original, label='Spectru Original',
             color=config.COLOR_ORIGINAL, linewidth=1.2, alpha=0.6)
    ax3.plot(freq_pos, fft_mag_filtered, label='Spectru Filtrat',
             color=config.COLOR_FILTERED, linewidth=2.5)
    ax3.set_xlabel('Frecventa (Hz)', fontsize=11, fontweight='bold')
    ax3.set_ylabel('Magnitudine (Amplitudine FFT)', fontsize=11, fontweight='bold')
    ax3.set_title('Comparatie Spectrala: Inainte si Dupa Filtrare\nObserva cum anumite frecvente au fost eliminate',
                  fontsize=12, fontweight='bold', pad=10)
    ax3.legend(loc='upper right', fontsize=11, framealpha=0.9)
    ax3.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
    ax3.set_xlim(0, sampling_freq / 2)

    # Text explicativ
    ax3.text(0.02, 0.95,
             'FFT (Fast Fourier Transform) descompune semnalul\nin componentele sale de frecventa',
             transform=ax3.transAxes, fontsize=10, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

    # Stilizare
    for ax in [ax1, ax2, ax3]:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_linewidth(1.5)
        ax.spines['bottom'].set_linewidth(1.5)

    plt.tight_layout()
    plt.show(block=False)


def plot_filter_response(frequencies, response, filter_type, cutoff_info):
    """
    Fereastra 3: Raspunsul in frecventa al filtrului

    Parameters:
    -----------
    frequencies : Vector de frecvente
    response : Raspunsul in frecventa
    filter_type : Tipul filtrului
    cutoff_info : Informatii despre frecventele de taiere
    """
    filter_names = {
        'lowpass': 'Trece-Jos',
        'highpass': 'Trece-Sus',
        'bandpass': 'Trece-Banda'
    }
    filter_name_ro = filter_names.get(filter_type.lower(), filter_type)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
    fig.canvas.manager.set_window_title('Caracteristica Filtrului')

    fig.suptitle(f'Caracteristica de Transfer - Filtru {filter_name_ro}\n{cutoff_info}',
                 fontsize=15, fontweight='bold')

    # Grafic 1: Raspuns in dB (scala logaritmica)
    magnitude_db = 20 * np.log10(np.abs(response) + 1e-10)
    ax1.plot(frequencies, magnitude_db, color=config.COLOR_SPECTRUM, linewidth=2.5)
    ax1.set_xlabel('Frecventa (Hz)', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Amplificare (dB)', fontsize=12, fontweight='bold')
    ax1.set_title('Raspuns in Magnitudine - Scala Logaritmica (dB)\nArata cat de mult sunt amplificate/atenuate diferitele frecvente',
                  fontsize=12, fontweight='bold')
    ax1.grid(True, alpha=0.4, linestyle='--')
    ax1.set_ylim(-100, 5)

    # Linia de -3dB (frecventa de taiere standard)
    ax1.axhline(y=-3, color='red', linestyle='--', linewidth=1.5, alpha=0.7, label='Prag -3dB (frecventa de taiere)')
    ax1.axhline(y=0, color='green', linestyle=':', linewidth=1, alpha=0.5, label='0dB (fara atenuare)')
    ax1.legend(fontsize=10, loc='upper right')

    # Text explicativ
    ax1.text(0.02, 0.05,
             '-3dB inseamna putere redusa la jumatate\n0dB inseamna semnal netransformat\n-20dB inseamna amplitudine redusa la 10%',
             transform=ax1.transAxes, fontsize=9, verticalalignment='bottom',
             bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

    # Grafic 2: Raspuns liniar
    ax2.plot(frequencies, np.abs(response), color=config.COLOR_SPECTRUM, linewidth=2.5)
    ax2.set_xlabel('Frecventa (Hz)', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Amplificare (factor)', fontsize=12, fontweight='bold')
    ax2.set_title('Raspuns in Magnitudine - Scala Liniara\nFactorul de amplificare pentru fiecare frecventa',
                  fontsize=12, fontweight='bold')
    ax2.grid(True, alpha=0.4, linestyle='--')

    # Linia de 0.707 (echivalent -3dB in scala liniara)
    ax2.axhline(y=0.707, color='red', linestyle='--', linewidth=1.5, alpha=0.7,
                label='0.707 (echivalent -3dB)')
    ax2.axhline(y=1.0, color='green', linestyle=':', linewidth=1, alpha=0.5,
                label='1.0 (fara atenuare)')
    ax2.legend(fontsize=10, loc='upper right')

    # Text explicativ
    ax2.text(0.02, 0.95,
             '1.0 = semnal netransformat\n0.707 = amplitudine la 70.7% (frecventa de taiere)\n0.1 = amplitudine redusa la 10%',
             transform=ax2.transAxes, fontsize=9, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))

    # Stilizare
    for ax in [ax1, ax2]:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_linewidth(1.5)
        ax.spines['bottom'].set_linewidth(1.5)

    plt.tight_layout()
    plt.show(block=False)



def show_all_plots():
    plt.show()