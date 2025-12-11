"""
Module pentru incarcarea datelor din fisiere CSV
"""
import pandas as pd
import numpy as np
from pathlib import Path


def load_signal_from_csv(filepath, time_column=0, signal_column=1, delimiter=','):
    """
    Incarca semnal din fisier CSV

    Parameters:
    -----------
    filepath : str
        Calea catre fisierul CSV
    time_column : int or str
        Index sau numele coloanei cu timp
    signal_column : int or str
        Index sau numele coloanei cu valori semnal
    delimiter : str
        Delimitator folosit in CSV (implicit ',')

    Returns:
    --------
    time : numpy.ndarray
        Vector cu valorile de timp
    signal : numpy.ndarray
        Vector cu valorile semnalului
    sampling_frequency : float
        Frecventa de esantionare calculata
    """
    file_path = Path(filepath)

    if not file_path.exists():
        raise FileNotFoundError(f"Fisierul nu exista: {filepath}")

    if file_path.suffix.lower() != '.csv':
        raise ValueError(f"Fisierul trebuie sa fie .csv, nu {file_path.suffix}")

    try:
        # Citeste CSV
        df = pd.read_csv(filepath, delimiter=delimiter)

        # Extrage coloanele
        if isinstance(time_column, int):
            time = df.iloc[:, time_column].values
        else:
            time = df[time_column].values

        if isinstance(signal_column, int):
            signal = df.iloc[:, signal_column].values
        else:
            signal = df[signal_column].values

        # Calculeaza frecventa de esantionare
        time_diff = np.diff(time)
        avg_time_step = np.mean(time_diff)
        sampling_frequency = 1.0 / avg_time_step if avg_time_step > 0 else 1.0

        print(f"Incarcat fisier CSV: {file_path.name}")
        print(f"  - Numar esantioane: {len(signal)}")
        print(f"  - Frecventa esantionare: {sampling_frequency:.2f} Hz")

        return time, signal, sampling_frequency

    except Exception as e:
        raise Exception(f"Eroare la citirea fisierului CSV: {str(e)}")


def save_signal(filepath, time, signal):
    """
    Salveaza semnalul intr-un fisier CSV

    Parameters:
    -----------
    filepath : str
        Calea unde se salveaza fisierul
    time : numpy.ndarray
        Vector cu valorile de timp
    signal : numpy.ndarray
        Vector cu valorile semnalului
    """
    df = pd.DataFrame({
        'timp': time,
        'semnal': signal
    })

    df.to_csv(filepath, index=False)

    print(f"Semnal salvat: {Path(filepath).name}")


def validate_csv_structure(filepath):
    """
    Valideaza structura fisierului CSV

    Parameters:
    -----------
    filepath : str
        Calea catre fisierul CSV

    Returns:
    --------
    bool
        True daca structura este valida
    str
        Mesaj de eroare sau succes
    """
    try:
        df = pd.read_csv(filepath)

        if df.shape[1] < 2:
            return False, "Fisierul trebuie sa contina cel putin 2 coloane (timp si semnal)"

        if df.empty:
            return False, "Fisierul este gol"

        # Verifica daca coloanele contin valori numerice
        if not np.issubdtype(df.iloc[:, 0].dtype, np.number):
            return False, "Prima coloana (timp) trebuie sa contina valori numerice"

        if not np.issubdtype(df.iloc[:, 1].dtype, np.number):
            return False, "A doua coloana (semnal) trebuie sa contina valori numerice"

        return True, "Structura fisier CSV valida"

    except Exception as e:
        return False, f"Eroare la validare: {str(e)}"