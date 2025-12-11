"""
Configurari globale pentru proiect
"""
import os

# Directoare
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_RAW_DIR = os.path.join(PROJECT_ROOT, 'data', 'raw')
DATA_PROCESSED_DIR = os.path.join(PROJECT_ROOT, 'data', 'processed')

# Parametri impliciti filtre
DEFAULT_FILTER_ORDER = 4
DEFAULT_SAMPLING_FREQUENCY = 1000  # Hz

# Parametri vizualizare
FIGURE_SIZE = (12, 6)
DPI = 100