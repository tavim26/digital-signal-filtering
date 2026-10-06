"""
Module pentru implementarea filtrelor digitale
"""
import numpy as np
from scipy.signal import butter, filtfilt, freqz


def lowpass_filter(data, cutoff_freq, sampling_freq, order=4):
    """
    Filtru trece-jos Butterworth

    Permite trecerea frecventelor sub cutoff_freq si elimina frecventele inalte.
    Util pentru: eliminarea zgomotului, netezirea semnalului.

    Parameters:
    data : Semnalul de intrare
    cutoff_freq : Frecventa de taiere (Hz)
    sampling_freq : Frecventa de esantionare (Hz)
    order : Ordinul filtrului (implicit 4)

    Returns:
    filtered_data : Semnalul filtrat
    """
    # VALIDARE PARAMETRI
    # -------------------
    # Frecventa Nyquist = jumatate din frecventa de esantionare
    # Este frecventa maxima care poate fi reprezentata corect in semnal
    # Teorema Nyquist: fs >= 2 * fmax
    nyquist = sampling_freq / 2.0

    # Verifica ca frecventa de taiere este sub Nyquist
    # Daca depaseste, filtrul nu poate functiona corect (aliasing)
    if cutoff_freq >= nyquist:
        raise ValueError(
            f"Frecventa de taiere ({cutoff_freq} Hz) trebuie sa fie mai mica decat frecventa Nyquist ({nyquist} Hz)")

    # NORMALIZARE FRECVENTA
    # ---------------------
    # Butterworth lucreaza cu frecvente normalizate in intervalul [0, 1]
    # unde 1 = frecventa Nyquist
    # Exemplu: daca cutoff = 50 Hz si Nyquist = 500 Hz => normalized = 0.1
    normalized_cutoff = cutoff_freq / nyquist

    # PROIECTARE FILTRU BUTTERWORTH
    # ------------------------------
    # butter() genereaza coeficientii filtrului digital
    # - order: ordinul filtrului (mai mare = tranzitie mai ascutita intre banda de trecere si banda oprita)
    # - normalized_cutoff: frecventa de taiere normalizata
    # - btype='low': tip filtru trece-jos (low-pass)
    # - analog=False: filtru digital (nu analog)
    # Returneaza:
    # - b: coeficientii numitorului (feedforward)
    # - a: coeficientii numaratorului (feedback)
    b, a = butter(order, normalized_cutoff, btype='low', analog=False)

    # APLICARE FILTRU
    # ---------------
    # filtfilt() aplica filtrul de 2 ori: inainte si inapoi
    # Avantaje:
    # 1. Faza zero: nu introduce intarziere in semnal
    # 2. Raspuns in magnitudine de 2x mai ascutit (ordin efectiv = 2 * order)
    # Alternative: lfilter() - aplica filtrul o singura data, introduce intarziere de faza
    filtered_data = filtfilt(b, a, data)

    print(f"Aplicat filtru trece-jos:")
    print(f"  - Frecventa taiere: {cutoff_freq} Hz")
    print(f"  - Ordin: {order}")

    return filtered_data



def highpass_filter(data, cutoff_freq, sampling_freq, order=4):
    """
    Filtru trece-sus Butterworth

    Permite trecerea frecventelor peste cutoff_freq si elimina frecventele joase.
    Util pentru: eliminarea componentei DC, eliminarea trend-urilor lente.

    Parameters:
    data : Semnalul de intrare
    cutoff_freq : Frecventa de taiere (Hz)
    sampling_freq : Frecventa de esantionare (Hz)
    order : Ordinul filtrului (implicit 4)

    Returns:
    filtered_data : Semnalul filtrat
    """
    # VALIDARE PARAMETRI
    # -------------------
    # Calculam frecventa Nyquist (limita superioara a spectrului)
    nyquist = sampling_freq / 2.0

    # Verificam ca frecventa de taiere este sub Nyquist
    # Nota: pentru highpass, cutoff trebuie sa fie > 0 si < Nyquist
    if cutoff_freq >= nyquist:
        raise ValueError(
            f"Frecventa de taiere ({cutoff_freq} Hz) trebuie sa fie mai mica decat frecventa Nyquist ({nyquist} Hz)")

    # NORMALIZARE FRECVENTA
    # ---------------------
    # Normalizare la intervalul [0, 1] pentru Butterworth
    normalized_cutoff = cutoff_freq / nyquist

    # PROIECTARE FILTRU BUTTERWORTH
    # ------------------------------
    # btype='high': tip filtru trece-sus (high-pass)
    # Elimina frecventele sub cutoff_freq
    # Folosit pentru: eliminare DC offset, eliminare drift lent, izolare frecvente inalte
    b, a = butter(order, normalized_cutoff, btype='high', analog=False)

    # APLICARE FILTRU
    # ---------------
    # filtfilt() asigura faza zero (fara intarziere)
    # Important pentru: analiza temporala precisa, sincronizare multi-semnal
    filtered_data = filtfilt(b, a, data)

    print(f"Aplicat filtru trece-sus:")
    print(f"  - Frecventa taiere: {cutoff_freq} Hz")
    print(f"  - Ordin: {order}")

    return filtered_data



def bandpass_filter(data, low_cutoff, high_cutoff, sampling_freq, order=4):
    """
    Filtru trece-banda Butterworth

    Permite trecerea frecventelor intre low_cutoff si high_cutoff.
    Util pentru: izolarea unei benzi specifice de frecvente.

    Parameters:
    data : Semnalul de intrare
    low_cutoff : Frecventa de taiere inferioara (Hz)
    high_cutoff : Frecventa de taiere superioara (Hz)
    sampling_freq : Frecventa de esantionare (Hz)
    order : Ordinul filtrului (implicit 4)

    Returns:
    filtered_data : Semnalul filtrat
    """
    # VALIDARE PARAMETRI
    # -------------------
    nyquist = sampling_freq / 2.0

    # Verifica ca frecventa inferioara < frecventa superioara
    # Altfel banda ar fi invalida
    if low_cutoff >= high_cutoff:
        raise ValueError("Frecventa inferioara trebuie sa fie mai mica decat frecventa superioara")

    # Verifica ca frecventa superioara este sub Nyquist
    # Ambele frecvente trebuie sa fie in domeniul valid [0, Nyquist]
    if high_cutoff >= nyquist:
        raise ValueError(
            f"Frecventa superioara ({high_cutoff} Hz) trebuie sa fie mai mica decat frecventa Nyquist ({nyquist} Hz)")

    # NORMALIZARE FRECVENTE
    # ---------------------
    # Normalizam AMBELE frecvente de taiere
    low_normalized = low_cutoff / nyquist
    high_normalized = high_cutoff / nyquist

    # PROIECTARE FILTRU BUTTERWORTH
    # ------------------------------
    # btype='band': tip filtru trece-banda (band-pass)
    # Parametru: lista cu 2 frecvente [low, high]
    # Rezultat: trec doar frecventele in intervalul [low_cutoff, high_cutoff]
    # Frecventele sub low_cutoff si peste high_cutoff sunt eliminate
    # Aplicatii: izolare ritm cardiac (ECG), filtrare vocala, analiza spectrala selectiva
    b, a = butter(order, [low_normalized, high_normalized], btype='band', analog=False)

    # APLICARE FILTRU
    # ---------------
    # filtfilt() pentru faza zero si raspuns mai ascutit
    filtered_data = filtfilt(b, a, data)

    print(f"Aplicat filtru trece-banda:")
    print(f"  - Frecventa inferioara: {low_cutoff} Hz")
    print(f"  - Frecventa superioara: {high_cutoff} Hz")
    print(f"  - Ordin: {order}")

    return filtered_data



