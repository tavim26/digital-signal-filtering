"""
Script principal pentru filtrarea semnalelor digitale cu interfata grafica
"""
import os
import sys

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

import config

# Importă modulele locale din src/
import data_loader
import filters
import visualization
import gui


def main():
    """
    Functia principala pentru procesarea semnalelor

    Flux de executie:
    1. Incarca date din CSV -> extrage timp, semnal, frecventa de esantionare
    2. Afiseaza GUI cu frecventa cunoscuta -> utilizatorul alege filtru si parametri
    3. Valideaza parametrii fata de frecventa Nyquist
    4. Aplica filtrul selectat pe semnal
    5. Salveaza rezultatul in CSV
    6. Genereaza 2 grafice: domeniu timp, domeniu frecventa
    """
    # ========== ETAPA 1: INCARCARE DATE ==========

    # Construieste calea completa catre fisierul de date
    # os.path.join() combina caile corect pentru orice sistem de operare (Windows/Linux/Mac)
    input_file = os.path.join(config.DATA_RAW_DIR, 'semnal_test.csv')

    try:
        # Incarca datele din CSV
        # Returneaza: time (vector timp), signal_data (vector semnal), sampling_freq (Hz)
        time, signal_data, sampling_freq = data_loader.load_signal_from_csv(input_file)

    except FileNotFoundError:
        # CAZUL 1: Fisierul nu exista
        # ---------------------------
        # Genereaza automat date de test pentru demonstratie
        print(f"Fisierul {input_file} nu exista. Generez date de test...")
        #generate_test_data()

        # Incearca din nou sa incarce datele (dupa generare)
        try:
            time, signal_data, sampling_freq = data_loader.load_signal_from_csv(input_file)
            print("Date de test incarcate cu succes!\n")
        except Exception as e:
            # Daca generarea sau incarcarea esueaza, opreste executia
            print(f"EROARE: Nu pot incarca datele: {str(e)}")
            return

    except Exception as e:
        # CAZUL 2: Alta eroare (fisier corupt, format invalid, etc.)
        # -----------------------------------------------------------
        print(f"EROARE: {str(e)}")
        return

    # ========== ETAPA 2: CONFIGURARE FILTRU PRIN GUI ==========

    # Afiseaza informatii despre semnal
    # Frecventa Nyquist = limita superioara pentru frecventele de taiere
    print(f"Frecventa Nyquist: {sampling_freq/2:.2f} Hz")
    print("Alege parametrii filtrului...\n")

    # Deschide interfata grafica pentru selectia filtrului
    # Returneaza:
    # - filter_type: 'lowpass', 'highpass', sau 'bandpass'
    # - params: dictionar cu parametrii (order, cutoff, low_cutoff, high_cutoff)
    filter_type, params = gui.get_filter_configuration(sampling_freq)

    # Verifica daca utilizatorul a anulat operatiunea
    if filter_type is None:
        print("Operatiune anulata.")
        return

    # ========== ETAPA 3: VALIDARE PARAMETRI ==========

    # Calculeaza frecventa Nyquist pentru validari
    # Toate frecventele de taiere TREBUIE sa fie < Nyquist
    nyquist = sampling_freq / 2

    # VALIDARE LOWPASS
    # ----------------
    # Verifica ca frecventa de taiere < Nyquist
    if filter_type == 'lowpass':
        if params.get('cutoff', 0) >= nyquist:
            print(f"EROARE: Frecventa de taiere ({params['cutoff']} Hz) >= Nyquist ({nyquist:.2f} Hz)")
            return

    # VALIDARE HIGHPASS
    # -----------------
    # Verifica ca frecventa de taiere < Nyquist
    elif filter_type == 'highpass':
        if params.get('cutoff', 0) >= nyquist:
            print(f"EROARE: Frecventa de taiere ({params['cutoff']} Hz) >= Nyquist ({nyquist:.2f} Hz)")
            return

    # VALIDARE BANDPASS
    # -----------------
    # Verifica 2 conditii:
    # 1. Frecventa superioara < Nyquist
    # 2. Frecventa inferioara < Frecventa superioara
    elif filter_type == 'bandpass':
        if params.get('high_cutoff', 0) >= nyquist:
            print(f"EROARE: Frecventa superioara ({params['high_cutoff']} Hz) >= Nyquist ({nyquist:.2f} Hz)")
            return
        if params.get('low_cutoff', 0) >= params.get('high_cutoff', 0):
            print(f"EROARE: Frecventa inferioara trebuie < frecventa superioara")
            return

    # ========== ETAPA 4: AFISARE PARAMETRI SELECTATI ==========

    # Dictionar pentru traducere nume filtre (ro)
    filter_names = {
        'lowpass': 'Trece-Jos',
        'highpass': 'Trece-Sus',
        'bandpass': 'Trece-Banda'
    }

    # Afiseaza informatii despre configuratia aleasa
    print(f"\nFiltru selectat: {filter_names[filter_type]}")
    print(f"Ordin: {params['order']}")
    print(f"Frecventa esantionare (din CSV): {sampling_freq:.2f} Hz")

    # Construieste string cu informatii specifice pentru fiecare tip de filtru
    # Acest string va fi afisat pe grafice pentru referinta
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

    # ========== ETAPA 5: APLICARE FILTRU ==========

    try:
        # CAZ 1: FILTRU TRECE-JOS
        # ------------------------
        # Elimina frecventele inalte (peste cutoff)
        # Pastreaza frecventele joase (sub cutoff)
        if filter_type == 'lowpass':
            filtered_signal = filters.lowpass_filter(signal_data, params['cutoff'],
                                                    sampling_freq, order=params['order'])

        # CAZ 2: FILTRU TRECE-SUS
        # ------------------------
        # Elimina frecventele joase (sub cutoff)
        # Pastreaza frecventele inalte (peste cutoff)
        elif filter_type == 'highpass':
            filtered_signal = filters.highpass_filter(signal_data, params['cutoff'],
                                                     sampling_freq, order=params['order'])

        # CAZ 3: FILTRU TRECE-BANDA
        # --------------------------
        # Elimina frecventele sub low_cutoff si peste high_cutoff
        # Pastreaza frecventele in intervalul [low_cutoff, high_cutoff]
        elif filter_type == 'bandpass':
            filtered_signal = filters.bandpass_filter(signal_data, params['low_cutoff'],
                                                     params['high_cutoff'],
                                                     sampling_freq, order=params['order'])

    except Exception as e:
        # Prinds erori de la functiile de filtrare (parametri invalizi, etc.)
        print(f"EROARE la filtrare: {str(e)}")
        return

    # ========== ETAPA 6: SALVARE REZULTATE ==========

    # Construieste numele fisierului de iesire
    # Format: semnal_<tip_filtru>_filtrat.csv
    output_file = os.path.join(config.DATA_PROCESSED_DIR, f'semnal_{filter_type}_filtrat.csv')

    # Salveaza semnalul filtrat in CSV (format: timp, semnal)
    data_loader.save_signal(output_file, time, filtered_signal)

    # ========== ETAPA 7: VIZUALIZARE REZULTATE ==========

    # GRAFIC 1: DOMENIUL TIMP
    # -----------------------
    # Compara semnalul original cu cel filtrat in domeniul timp
    # 3 subgrafice: original, filtrat, suprapunere
    visualization.plot_time_domain_comparison(time, signal_data, filtered_signal,
                                             filter_type, cutoff_info)

    # GRAFIC 2: DOMENIUL FRECVENTA (FFT)
    # -----------------------------------
    # Compara spectrul de frecventa inainte si dupa filtrare
    # Arata cum filtrul elimina anumite componente de frecventa
    # 3 subgrafice: spectru original, spectru filtrat, suprapunere
    visualization.plot_frequency_domain_comparison(time, signal_data, filtered_signal,
                                                  sampling_freq, filter_type, cutoff_info)


    # AFISARE GRAFICE
    # ---------------
    # Blocheaza executia pana cand utilizatorul inchide ferestrele
    # Fara aceasta linie, graficele ar disparea imediat
    visualization.show_all_plots()

    print("Procesare finalizata.\n")



# ENTRY POINT

if __name__ == "__main__":
    main()