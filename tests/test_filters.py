"""
Teste unitare pentru modulul de filtrare
"""
import numpy as np
import sys
import os

# Adauga calea catre directorul src
src_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src')
sys.path.insert(0, src_path)

import filters


def test_lowpass_filter():
    """
    Test pentru filtrul trece-jos
    """
    print("Test: Filtru trece-jos...")

    # Genereaza semnal de test
    fs = 1000  # Hz
    t = np.linspace(0, 1, fs)
    signal = np.sin(2 * np.pi * 5 * t) + np.sin(2 * np.pi * 50 * t)

    # Aplica filtru
    filtered = filters.lowpass_filter(signal, cutoff_freq=20, sampling_freq=fs, order=4)

    # Verifica
    assert len(filtered) == len(signal), "Lungimea semnalului filtrat este incorecta"
    assert not np.isnan(filtered).any(), "Semnalul filtrat contine NaN"

    print("  -> PASSED")


def test_highpass_filter():
    """
    Test pentru filtrul trece-sus
    """
    print("Test: Filtru trece-sus...")

    # Genereaza semnal de test
    fs = 1000  # Hz
    t = np.linspace(0, 1, fs)
    signal = np.sin(2 * np.pi * 5 * t) + np.sin(2 * np.pi * 50 * t)

    # Aplica filtru
    filtered = filters.highpass_filter(signal, cutoff_freq=20, sampling_freq=fs, order=4)

    # Verifica
    assert len(filtered) == len(signal), "Lungimea semnalului filtrat este incorecta"
    assert not np.isnan(filtered).any(), "Semnalul filtrat contine NaN"

    print("  -> PASSED")


def test_bandpass_filter():
    """
    Test pentru filtrul trece-banda
    """
    print("Test: Filtru trece-banda...")

    # Genereaza semnal de test
    fs = 1000  # Hz
    t = np.linspace(0, 1, fs)
    signal = np.sin(2 * np.pi * 5 * t) + np.sin(2 * np.pi * 50 * t) + np.sin(2 * np.pi * 200 * t)

    # Aplica filtru
    filtered = filters.bandpass_filter(signal, low_cutoff=20, high_cutoff=100, sampling_freq=fs, order=4)

    # Verifica
    assert len(filtered) == len(signal), "Lungimea semnalului filtrat este incorecta"
    assert not np.isnan(filtered).any(), "Semnalul filtrat contine NaN"

    print("  -> PASSED")


def run_all_tests():
    """
    Ruleaza toate testele
    """
    print("\n" + "=" * 50)
    print("RULARE TESTE UNITARE")
    print("=" * 50 + "\n")

    test_lowpass_filter()
    test_highpass_filter()
    test_bandpass_filter()

    print("\n" + "=" * 50)
    print("TOATE TESTELE AU TRECUT CU SUCCES!")
    print("=" * 50 + "\n")


if __name__ == "__main__":
    run_all_tests()