"""
Script principal pentru filtrarea semnalelor digitale
"""
import os
import sys
import numpy as np
from pathlib import Path

# Import module locale
from data_loader import load_signal_from_csv, save_signal
from filters import lowpass_filter, highpass_filter, bandpass_filter, get_filter_response
from visualization import plot_signals, plot_frequency_spectrum, plot_filter_response, plot_all_analysis

# Import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config


def main():
    """
    Functia principala pentru procesarea semnalelor
    """
    print("=" * 70)
    print("SISTEM DE FILTRARE SEMNALE DIGITALE")
    print("=" * 70)
    print()

    # ========== CONFIGURARE ==========

    # Calea catre fisierul de intrare (modifica cu fisierul tau)
    input_file = os.path.join(config.DATA_RAW_DIR, 'semnal_test.csv')

    # Parametri filtru
    filter_order = 4

    # Frecvente de taiere (modifica dupa necesitati)
    lowpass_cutoff = 50  # Hz - pentru filtru trece-jos
    highpass_cutoff = 10  # Hz - pentru filtru trece-sus
    bandpass_low = 20  # Hz - pentru filtru trece-banda
    bandpass_high = 80  # Hz - pentru filtru trece-banda

    # Tipul de filtru de aplicat: 'lowpass', 'highpass', 'bandpass'
    filter_type = 'lowpass'

    # ========== INCARCARE DATE ==========

    print(f"Incarcare date din: {input_file}")
    print()

    try:
        time, signal_data, sampling_freq = load_signal_from_csv(input_file)
        print()
    except FileNotFoundError:
        print(f"EROARE: Fisierul {input_file} nu exista!")
        print(f"Asigura-te ca ai un fisier CSV in directorul: {config.DATA_RAW_DIR}")
        print()
        print("Generare date de test...")
        generate_test_data()
        return
    except Exception as e:
        print(f"EROARE la incarcarea datelor: {str(e)}")
        return

    # ========== APLICARE FILTRU ==========

    print(f"Aplicare filtru: {filter_type.upper()}")
    print(f"Frecventa esantionare: {sampling_freq:.2f} Hz")
    print(f"Frecventa Nyquist: {sampling_freq / 2:.2f} Hz")
    print()

    try:
        if filter_type == 'lowpass':
            filtered_signal = lowpass_filter(signal_data, lowpass_cutoff, sampling_freq, order=filter_order)
            cutoff_info = f"Frecventa taiere: {lowpass_cutoff} Hz"

        elif filter_type == 'highpass':
            filtered_signal = highpass_filter(signal_data, highpass_cutoff, sampling_freq, order=filter_order)
            cutoff_info = f"Frecventa taiere: {highpass_cutoff} Hz"

        elif filter_type == 'bandpass':
            filtered_signal = bandpass_filter(signal_data, bandpass_low, bandpass_high,
                                              sampling_freq, order=filter_order)
            cutoff_info = f"Banda: {bandpass_low} - {bandpass_high} Hz"
        else:
            print(f"EROARE: Tip filtru necunoscut: {filter_type}")
            return

        print()

    except Exception as e:
        print(f"EROARE la aplicarea filtrului: {str(e)}")
        return

    # ========== SALVARE REZULTATE ==========

    output_file = os.path.join(config.DATA_PROCESSED_DIR, f'semnal_{filter_type}_filtrat.csv')
    save_signal(output_file, time, filtered_signal)
    print()

    # ========== VIZUALIZARE ==========

    print("Generare grafice...")
    print()

    # Grafic comparativ semnal temporal
    plot_signals(time, signal_data, filtered_signal,
                 title=f"Comparatie: Filtru {filter_type.upper()}")

    # Spectru de frecventa
    plot_frequency_spectrum(time, signal_data, filtered_signal, sampling_freq,
                            title=f"Analiza Frecventa - Filtru {filter_type.upper()}")

    # Raspuns filtru
    if filter_type == 'bandpass':
        freq_response, mag_response = get_filter_response(filter_type, None, sampling_freq,
                                                          filter_order, bandpass_low, bandpass_high)
    else:
        cutoff = lowpass_cutoff if filter_type == 'lowpass' else highpass_cutoff
        freq_response, mag_response = get_filter_response(filter_type, cutoff, sampling_freq, filter_order)

    plot_filter_response(freq_response, mag_response, filter_type.upper(), cutoff_info)

    # Analiza completa
    plot_all_analysis(time, signal_data, filtered_signal, sampling_freq,
                      filter_type.upper(), cutoff_info)

    print("=" * 70)
    print("PROCESARE FINALIZATA CU SUCCES!")
    print("=" * 70)


def generate_test_data():
    """
    Genereaza date de test pentru demonstratie
    """
    print()
    print("Generare semnal de test...")

    # Parametri semnal
    duration = 2.0  # secunde
    sampling_freq = 1000  # Hz
    t = np.linspace(0, duration, int(sampling_freq * duration))

    # Semnal compozit: ton de 5 Hz + ton de 50 Hz + zgomot
    signal_clean = np.sin(2 * np.pi * 5 * t) + 0.5 * np.sin(2 * np.pi * 50 * t)
    noise = np.random.normal(0, 0.2, len(t))
    signal_noisy = signal_clean + noise

    # Salvare
    output_file = os.path.join(config.DATA_RAW_DIR, 'semnal_test.csv')
    save_signal(output_file, t, signal_noisy)

    print()
    print(f"Semnal de test generat: {output_file}")
    print("Ruleaza din nou programul pentru a-l procesa!")
    print()


if __name__ == "__main__":
    main()
