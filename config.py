"""
Configurari globale pentru proiectul de filtrare semnale digitale
"""
import os

# Directoare proiect
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_RAW_DIR = os.path.join(PROJECT_ROOT, 'data', 'raw')
DATA_PROCESSED_DIR = os.path.join(PROJECT_ROOT, 'data', 'processed')

# Parametri impliciti pentru filtre
DEFAULT_FILTER_ORDER = 4
DEFAULT_SAMPLING_FREQUENCY = 1000  # Hz

# Parametri vizualizare
FIGURE_SIZE = (14, 8)
DPI = 100

# Culori pentru grafice
COLOR_ORIGINAL = '#2E86AB'
COLOR_FILTERED = '#A23B72'
COLOR_SPECTRUM = '#F18F01'