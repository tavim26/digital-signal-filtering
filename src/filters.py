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
    # Valideaza parametrii
    nyquist = sampling_freq / 2.0
    if cutoff_freq >= nyquist:
        raise ValueError(
            f"Frecventa de taiere ({cutoff_freq} Hz) trebuie sa fie mai mica decat frecventa Nyquist ({nyquist} Hz)")

    # Normalizeaza frecventa de taiere
    normalized_cutoff = cutoff_freq / nyquist

    # Proiecteaza filtrul Butterworth
    b, a = butter(order, normalized_cutoff, btype='low', analog=False)

    # Aplica filtrul (filtfilt pentru faza zero)
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
    # Valideaza parametrii
    nyquist = sampling_freq / 2.0
    if cutoff_freq >= nyquist:
        raise ValueError(
            f"Frecventa de taiere ({cutoff_freq} Hz) trebuie sa fie mai mica decat frecventa Nyquist ({nyquist} Hz)")

    # Normalizeaza frecventa de taiere
    normalized_cutoff = cutoff_freq / nyquist

    # Proiecteaza filtrul Butterworth
    b, a = butter(order, normalized_cutoff, btype='high', analog=False)

    # Aplica filtrul
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
    # Valideaza parametrii
    nyquist = sampling_freq / 2.0

    if low_cutoff >= high_cutoff:
        raise ValueError("Frecventa inferioara trebuie sa fie mai mica decat frecventa superioara")

    if high_cutoff >= nyquist:
        raise ValueError(
            f"Frecventa superioara ({high_cutoff} Hz) trebuie sa fie mai mica decat frecventa Nyquist ({nyquist} Hz)")

    # Normalizeaza frecventele de taiere
    low_normalized = low_cutoff / nyquist
    high_normalized = high_cutoff / nyquist

    # Proiecteaza filtrul Butterworth
    b, a = butter(order, [low_normalized, high_normalized], btype='band', analog=False)

    # Aplica filtrul
    filtered_data = filtfilt(b, a, data)

    print(f"Aplicat filtru trece-banda:")
    print(f"  - Frecventa inferioara: {low_cutoff} Hz")
    print(f"  - Frecventa superioara: {high_cutoff} Hz")
    print(f"  - Ordin: {order}")

    return filtered_data




def get_filter_response(filter_type, cutoff_freq, sampling_freq, order=4, low_cutoff=None, high_cutoff=None):
    """
    Calculeaza raspunsul in frecventa al filtrului

    Parameters:
    filter_type : Tipul filtrului: 'lowpass', 'highpass', sau 'bandpass'
    cutoff_freq : Frecventa de taiere (pentru lowpass si highpass)
    sampling_freq : Frecventa de esantionare
    order : Ordinul filtrului
    low_cutoff : Frecventa inferioara (pentru bandpass)
    high_cutoff : Frecventa superioara (pentru bandpass)

    Returns:
    frequencies : Vectorul de frecvente
    response : Raspunsul in frecventa (magnitudine)
    """
    nyquist = sampling_freq / 2.0

    if filter_type == 'lowpass':
        normalized_cutoff = cutoff_freq / nyquist
        b, a = butter(order, normalized_cutoff, btype='low')
    elif filter_type == 'highpass':
        normalized_cutoff = cutoff_freq / nyquist
        b, a = butter(order, normalized_cutoff, btype='high')
    elif filter_type == 'bandpass':
        low_normalized = low_cutoff / nyquist
        high_normalized = high_cutoff / nyquist
        b, a = butter(order, [low_normalized, high_normalized], btype='band')
    else:
        raise ValueError(f"Tip filtru necunoscut: {filter_type}")

    # Calculeaza raspunsul in frecventa
    w, h = freqz(b, a, worN=8000)
    frequencies = w * sampling_freq / (2 * np.pi)
    response = np.abs(h)

    return frequencies, response