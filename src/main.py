"""
Script principal pentru filtrarea semnalelor digitale cu interfata grafica
"""
import os
import sys
import numpy as np

# Adaugă directorul părinte (rădăcina proiectului) la sys.path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Importă config din rădăcină
import config

# Importă modulele locale din src/
import data_loader
import filters
import visualization
import gui


def main():
    """
    Functia principala pentru procesarea semnalelor
    """
    # ========== INCARCARE DATE MAI ÎNTÂI ==========

    input_file = os.path.join(config.DATA_RAW_DIR, 'semnal_test.csv')

    try:
        time, signal_data, sampling_freq = data_loader.load_signal_from_csv(input_file)
    except FileNotFoundError:
        print(f"Fisierul {input_file} nu exista. Generez date de test...")
        generate_test_data()
        # Încearcă din nou să încarce
        try:
            time, signal_data, sampling_freq = data_loader.load_signal_from_csv(input_file)
            print("Date de test incarcate cu succes!\n")
        except Exception as e:
            print(f"EROARE: Nu pot incarca datele: {str(e)}")
            return
    except Exception as e:
        print(f"EROARE: {str(e)}")
        return

    # ========== ACUM AFISEAZA GUI CU FRECVENȚA CUNOSCUTA ==========

    print(f"Frecventa Nyquist: {sampling_freq/2:.2f} Hz")
    print("Alege parametrii filtrului...\n")

    filter_type, params = gui.get_filter_configuration(sampling_freq)

    if filter_type is None:
        print("Operatiune anulata.")
        return

    # ========== VALIDARE FRECVENȚE DE TAIERE ==========

    nyquist = sampling_freq / 2

    if filter_type == 'lowpass':
        if params.get('cutoff', 0) >= nyquist:
            print(f"EROARE: Frecventa de taiere ({params['cutoff']} Hz) >= Nyquist ({nyquist:.2f} Hz)")
            return

    elif filter_type == 'highpass':
        if params.get('cutoff', 0) >= nyquist:
            print(f"EROARE: Frecventa de taiere ({params['cutoff']} Hz) >= Nyquist ({nyquist:.2f} Hz)")
            return

    elif filter_type == 'bandpass':
        if params.get('high_cutoff', 0) >= nyquist:
            print(f"EROARE: Frecventa superioara ({params['high_cutoff']} Hz) >= Nyquist ({nyquist:.2f} Hz)")
            return
        if params.get('low_cutoff', 0) >= params.get('high_cutoff', 0):
            print(f"EROARE: Frecventa inferioara trebuie < frecventa superioara")
            return

    # ========== AFIȘARE PARAMETRI SELECTATI ==========

    filter_names = {
        'lowpass': 'Trece-Jos',
        'highpass': 'Trece-Sus',
        'bandpass': 'Trece-Banda'
    }

    print(f"\nFiltru selectat: {filter_names[filter_type]}")
    print(f"Ordin: {params['order']}")
    print(f"Frecventa esantionare (din CSV): {sampling_freq:.2f} Hz")

    if filter_type == 'lowpass':
        print(f"Frecventa taiere: {params['cutoff']} Hz")
        cutoff_info = f"Frecventa taiere: {params['cutoff']} Hz, Ordin: {params['order']}"
    elif filter_type == 'highpass':
        print(f"Frecventa taiere: {params['cutoff']} Hz")
        cutoff_info = f"Frecventa taiere: {params['cutoff']} Hz, Ordin: {params['order']}"
    elif filter_type == 'bandpass':
        print(f"Banda: {params['low_cutoff']} - {params['high_cutoff']} Hz")
        cutoff_info = f"Banda: {params['low_cutoff']} - {params['high_cutoff']} Hz, Ordin: {params['order']}"

    print()

    # ========== APLICARE FILTRU ==========

    try:
        if filter_type == 'lowpass':
            filtered_signal = filters.lowpass_filter(signal_data, params['cutoff'],
                                                    sampling_freq, order=params['order'])

        elif filter_type == 'highpass':
            filtered_signal = filters.highpass_filter(signal_data, params['cutoff'],
                                                     sampling_freq, order=params['order'])

        elif filter_type == 'bandpass':
            filtered_signal = filters.bandpass_filter(signal_data, params['low_cutoff'],
                                                     params['high_cutoff'],
                                                     sampling_freq, order=params['order'])

    except Exception as e:
        print(f"EROARE la filtrare: {str(e)}")
        return

    # ========== SALVARE REZULTATE ==========

    output_file = os.path.join(config.DATA_PROCESSED_DIR, f'semnal_{filter_type}_filtrat.csv')
    data_loader.save_signal(output_file, time, filtered_signal)

    # ========== VIZUALIZARE ==========

    visualization.plot_time_domain_comparison(time, signal_data, filtered_signal,
                                             filter_type, cutoff_info)

    visualization.plot_frequency_domain_comparison(time, signal_data, filtered_signal,
                                                  sampling_freq, filter_type, cutoff_info)

    if filter_type == 'bandpass':
        freq_response, mag_response = filters.get_filter_response(
            filter_type, None, sampling_freq, params['order'],
            params['low_cutoff'], params['high_cutoff'])
    else:
        freq_response, mag_response = filters.get_filter_response(
            filter_type, params['cutoff'], sampling_freq, params['order'])

    visualization.plot_filter_response(freq_response, mag_response, filter_type, cutoff_info)

    visualization.show_all_plots()

    print("Procesare finalizata.\n")


def generate_test_data():
    """Genereaza date de test"""
    duration = 2.0
    sampling_freq = 1000
    t = np.linspace(0, duration, int(sampling_freq * duration))

    signal_clean = np.sin(2 * np.pi * 5 * t) + 0.5 * np.sin(2 * np.pi * 50 * t)
    noise = np.random.normal(0, 0.2, len(t))
    signal_noisy = signal_clean + noise

    output_file = os.path.join(config.DATA_RAW_DIR, 'semnal_test.csv')
    data_loader.save_signal(output_file, t, signal_noisy)
    print(f"Semnal de test generat: {output_file}")


if __name__ == "__main__":
    main()