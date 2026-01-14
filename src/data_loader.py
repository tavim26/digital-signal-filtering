"""
Module pentru incarcarea datelor din fisiere CSV
"""
import pandas as pd
import numpy as np
from pathlib import Path


def load_signal_from_csv(filepath, time_column=0, signal_column=1, delimiter=','):
    """
    Incarca semnal din fisier CSV

    """
    # CONVERSIE LA PATH OBJECT
    # ------------------------
    # Path() din pathlib ofera metode utile pentru manipulare fisiere
    file_path = Path(filepath)

    # VALIDARE EXISTENTA FISIER
    # -------------------------
    # Verifica daca fisierul exista pe disc inainte de a incerca citirea
    # Previne erori confuze de la pandas
    if not file_path.exists():
        raise FileNotFoundError(f"Fisierul nu exista: {filepath}")

    # VALIDARE EXTENSIE FISIER
    # ------------------------
    # Verifica ca fisierul are extensia .csv
    if file_path.suffix.lower() != '.csv':
        raise ValueError(f"Fisierul trebuie sa fie .csv, nu {file_path.suffix}")

    try:
        # CITIRE FISIER CSV
        # -----------------
        # pandas.read_csv() citeste fisierul si il transforma in DataFrame
        # DataFrame = tabel cu randuri si coloane, similar cu Excel
        df = pd.read_csv(filepath, delimiter=delimiter)

        # EXTRAGERE COLOANA TIMP
        # ----------------------
        # Suporta 2 moduri de selectie:
        # 1. Index numeric (ex: 0 = prima coloana)
        # 2. Nume coloana (ex: "timp", "time", etc.)
        if isinstance(time_column, int):
            # .iloc[:, index] = selecteaza toate randurile (:) din coloana index
            # .values = converteste din pandas Series in numpy array
            time = df.iloc[:, time_column].values
        else:
            # df[nume_coloana] = selecteaza coloana dupa nume
            time = df[time_column].values

        # EXTRAGERE COLOANA SEMNAL
        # ------------------------
        # Acelasi mecanism ca pentru coloana timp
        # Rezultat: numpy array cu valorile semnalului
        if isinstance(signal_column, int):
            signal = df.iloc[:, signal_column].values
        else:
            signal = df[signal_column].values

        # CALCUL FRECVENTA DE ESANTIONARE
        # --------------------------------
        # Pasul 1: Calculeaza diferentele dintre timpi consecutivi
        # np.diff([0.000, 0.001, 0.002]) = [0.001, 0.001]
        # Aceasta este perioada de esantionare (Ts sau dt)
        time_diff = np.diff(time)

        # Pasul 2: Calculeaza perioada medie de esantionare
        # Daca esantionarea este uniforma, toate valorile din time_diff sunt egale
        # Media elimina eventuale erori mici de rotunjire
        avg_time_step = np.mean(time_diff)

        # Pasul 3: Calculeaza frecventa de esantionare
        # Formula: fs = 1 / Ts
        # Exemplu: daca Ts = 0.001 s => fs = 1000 Hz
        # Protectie: daca avg_time_step = 0 (date invalide), returneaza 1.0 Hz implicit
        sampling_frequency = 1.0 / avg_time_step if avg_time_step > 0 else 1.0

        # AFISARE INFORMATII
        print(f"Incarcat fisier CSV: {file_path.name}")
        print(f"  - Numar esantioane: {len(signal)}")
        print(f"  - Frecventa esantionare: {sampling_frequency:.2f} Hz")

        # RETURNARE DATE
        # --------------
        # time: vector cu timpii de esantionare
        # signal: vector cu valorile semnalului
        # sampling_frequency: frecventa calculata automat
        return time, signal, sampling_frequency

    except Exception as e:
        # GESTIONARE ERORI
        raise Exception(f"Eroare la citirea fisierului CSV: {str(e)}")


def save_signal(filepath, time, signal):
    """
    Salveaza semnalul intr-un fisier CSV

    """
    # CREARE DATAFRAME
    # ----------------
    # Construieste un tabel pandas cu 2 coloane: 'timp' si 'semnal'
    # Dicionar: cheile devin numele coloanelor, valorile devin datele

    df = pd.DataFrame({
        'timp': time,
        'semnal': signal
    })

    # SALVARE IN FISIER CSV
    # ---------------------
    # .to_csv() scrie DataFrame-ul in fisier
    # Rezultat: fisier CSV cu header (timp,semnal) si date
    df.to_csv(filepath, index=False)


    print(f"Semnal salvat: {Path(filepath).name}")

