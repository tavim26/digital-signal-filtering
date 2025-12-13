"""
Interfata grafica profesionista pentru configurarea filtrului
"""
import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config


class FilterGUI:
    """
    Interfata grafica profesionista pentru selectia si configurarea filtrului
    """

    def __init__(self):
        self.selected_filter = None
        self.filter_params = {}

        self.root = tk.Tk()
        self.root.title("Configurare Filtru Digital")
        self.root.geometry("600x700")
        self.root.resizable(False, False)
        self.root.configure(bg='#f5f5f5')

        # Centreaza fereastra
        self.center_window()

        # Variabile pentru parametri
        self.filter_type_var = tk.StringVar(value="")
        self.order_var = tk.IntVar(value=4)
        self.lowpass_cutoff_var = tk.DoubleVar(value=50.0)
        self.highpass_cutoff_var = tk.DoubleVar(value=10.0)
        self.bandpass_low_var = tk.DoubleVar(value=20.0)
        self.bandpass_high_var = tk.DoubleVar(value=80.0)
        self.sampling_freq_var = tk.DoubleVar(value=1000.0)

        self.create_widgets()

    def center_window(self):
        """Centreaza fereastra pe ecran"""
        self.root.update_idletasks()
        width = 600
        height = 700
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def create_widgets(self):
        """Creaza elementele interfetei"""

        # ========== HEADER ==========
        header_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        title_label = tk.Label(
            header_frame,
            text="Configurare Filtru Digital",
            font=('Segoe UI', 20, 'bold'),
            bg='#2c3e50',
            fg='white'
        )
        title_label.pack(pady=20)

        # ========== MAIN CONTENT ==========
        main_frame = tk.Frame(self.root, bg='#f5f5f5')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

        # --- Sectiune 1: Tipul Filtrului ---
        section1 = tk.LabelFrame(
            main_frame,
            text="1. Selecteaza Tipul de Filtru",
            font=('Segoe UI', 11, 'bold'),
            bg='#f5f5f5',
            fg='#2c3e50',
            padx=15,
            pady=15
        )
        section1.pack(fill=tk.X, pady=(0, 20))

        filter_types = [
            ("Filtru Trece-Jos (elimina frecvente inalte)", "lowpass", "#3498db"),
            ("Filtru Trece-Sus (elimina frecvente joase)", "highpass", "#e74c3c"),
            ("Filtru Trece-Banda (pastreaza o banda)", "bandpass", "#f39c12")
        ]

        for text, value, color in filter_types:
            rb = tk.Radiobutton(
                section1,
                text=text,
                variable=self.filter_type_var,
                value=value,
                font=('Segoe UI', 10),
                bg='#f5f5f5',
                activebackground='#f5f5f5',
                selectcolor=color,
                command=self.on_filter_type_change
            )
            rb.pack(anchor=tk.W, pady=5)

        # --- Sectiune 2: Parametri Generali ---
        section2 = tk.LabelFrame(
            main_frame,
            text="2. Parametri Generali",
            font=('Segoe UI', 11, 'bold'),
            bg='#f5f5f5',
            fg='#2c3e50',
            padx=15,
            pady=15
        )
        section2.pack(fill=tk.X, pady=(0, 20))

        # Ordinul filtrului
        order_frame = tk.Frame(section2, bg='#f5f5f5')
        order_frame.pack(fill=tk.X, pady=5)

        tk.Label(
            order_frame,
            text="Ordinul Filtrului:",
            font=('Segoe UI', 10),
            bg='#f5f5f5',
            width=20,
            anchor='w'
        ).pack(side=tk.LEFT)

        order_spinbox = tk.Spinbox(
            order_frame,
            from_=2,
            to=8,
            increment=2,
            textvariable=self.order_var,
            font=('Segoe UI', 10),
            width=10
        )
        order_spinbox.pack(side=tk.LEFT, padx=10)

        tk.Label(
            order_frame,
            text="(2-8, ordin mai mare = tranzitie mai ascutita)",
            font=('Segoe UI', 8),
            bg='#f5f5f5',
            fg='#7f8c8d'
        ).pack(side=tk.LEFT)

        # Frecventa de esantionare
        fs_frame = tk.Frame(section2, bg='#f5f5f5')
        fs_frame.pack(fill=tk.X, pady=5)

        tk.Label(
            fs_frame,
            text="Frecventa Esantionare:",
            font=('Segoe UI', 10),
            bg='#f5f5f5',
            width=20,
            anchor='w'
        ).pack(side=tk.LEFT)

        fs_entry = tk.Entry(
            fs_frame,
            textvariable=self.sampling_freq_var,
            font=('Segoe UI', 10),
            width=10
        )
        fs_entry.pack(side=tk.LEFT, padx=10)

        tk.Label(
            fs_frame,
            text="Hz (din fisierul CSV)",
            font=('Segoe UI', 8),
            bg='#f5f5f5',
            fg='#7f8c8d'
        ).pack(side=tk.LEFT)

        # --- Sectiune 3: Frecvente de Taiere ---
        self.section3 = tk.LabelFrame(
            main_frame,
            text="3. Frecvente de Taiere",
            font=('Segoe UI', 11, 'bold'),
            bg='#f5f5f5',
            fg='#2c3e50',
            padx=15,
            pady=15
        )
        self.section3.pack(fill=tk.X, pady=(0, 20))

        # Frame pentru lowpass
        self.lowpass_frame = tk.Frame(self.section3, bg='#f5f5f5')

        tk.Label(
            self.lowpass_frame,
            text="Frecventa Taiere:",
            font=('Segoe UI', 10),
            bg='#f5f5f5',
            width=20,
            anchor='w'
        ).pack(side=tk.LEFT)

        tk.Entry(
            self.lowpass_frame,
            textvariable=self.lowpass_cutoff_var,
            font=('Segoe UI', 10),
            width=10
        ).pack(side=tk.LEFT, padx=10)

        tk.Label(
            self.lowpass_frame,
            text="Hz (frecvente peste aceasta sunt eliminate)",
            font=('Segoe UI', 8),
            bg='#f5f5f5',
            fg='#7f8c8d'
        ).pack(side=tk.LEFT)

        # Frame pentru highpass
        self.highpass_frame = tk.Frame(self.section3, bg='#f5f5f5')

        tk.Label(
            self.highpass_frame,
            text="Frecventa Taiere:",
            font=('Segoe UI', 10),
            bg='#f5f5f5',
            width=20,
            anchor='w'
        ).pack(side=tk.LEFT)

        tk.Entry(
            self.highpass_frame,
            textvariable=self.highpass_cutoff_var,
            font=('Segoe UI', 10),
            width=10
        ).pack(side=tk.LEFT, padx=10)

        tk.Label(
            self.highpass_frame,
            text="Hz (frecvente sub aceasta sunt eliminate)",
            font=('Segoe UI', 8),
            bg='#f5f5f5',
            fg='#7f8c8d'
        ).pack(side=tk.LEFT)

        # Frame pentru bandpass
        self.bandpass_frame = tk.Frame(self.section3, bg='#f5f5f5')

        bp_low_frame = tk.Frame(self.bandpass_frame, bg='#f5f5f5')
        bp_low_frame.pack(fill=tk.X, pady=5)

        tk.Label(
            bp_low_frame,
            text="Frecventa Inferioara:",
            font=('Segoe UI', 10),
            bg='#f5f5f5',
            width=20,
            anchor='w'
        ).pack(side=tk.LEFT)

        tk.Entry(
            bp_low_frame,
            textvariable=self.bandpass_low_var,
            font=('Segoe UI', 10),
            width=10
        ).pack(side=tk.LEFT, padx=10)

        tk.Label(
            bp_low_frame,
            text="Hz",
            font=('Segoe UI', 8),
            bg='#f5f5f5',
            fg='#7f8c8d'
        ).pack(side=tk.LEFT)

        bp_high_frame = tk.Frame(self.bandpass_frame, bg='#f5f5f5')
        bp_high_frame.pack(fill=tk.X, pady=5)

        tk.Label(
            bp_high_frame,
            text="Frecventa Superioara:",
            font=('Segoe UI', 10),
            bg='#f5f5f5',
            width=20,
            anchor='w'
        ).pack(side=tk.LEFT)

        tk.Entry(
            bp_high_frame,
            textvariable=self.bandpass_high_var,
            font=('Segoe UI', 10),
            width=10
        ).pack(side=tk.LEFT, padx=10)

        tk.Label(
            bp_high_frame,
            text="Hz",
            font=('Segoe UI', 8),
            bg='#f5f5f5',
            fg='#7f8c8d'
        ).pack(side=tk.LEFT)

        # Initial ascunde toate frame-urile de parametri
        self.lowpass_frame.pack_forget()
        self.highpass_frame.pack_forget()
        self.bandpass_frame.pack_forget()

        # --- Butoane ---
        button_frame = tk.Frame(main_frame, bg='#f5f5f5')
        button_frame.pack(fill=tk.X, pady=(20, 0))

        apply_btn = tk.Button(
            button_frame,
            text="Aplica Filtrarea",
            font=('Segoe UI', 12, 'bold'),
            bg='#27ae60',
            fg='white',
            activebackground='#229954',
            activeforeground='white',
            cursor='hand2',
            relief=tk.FLAT,
            padx=30,
            pady=15,
            command=self.apply_filter
        )
        apply_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))

        cancel_btn = tk.Button(
            button_frame,
            text="Anuleaza",
            font=('Segoe UI', 12),
            bg='#95a5a6',
            fg='white',
            activebackground='#7f8c8d',
            activeforeground='white',
            cursor='hand2',
            relief=tk.FLAT,
            padx=30,
            pady=15,
            command=self.cancel
        )
        cancel_btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(5, 0))

    def on_filter_type_change(self):
        """Handler pentru schimbarea tipului de filtru"""
        filter_type = self.filter_type_var.get()

        # Ascunde toate frame-urile
        self.lowpass_frame.pack_forget()
        self.highpass_frame.pack_forget()
        self.bandpass_frame.pack_forget()

        # Afiseaza frame-ul corespunzator
        if filter_type == 'lowpass':
            self.lowpass_frame.pack(fill=tk.X, pady=5)
        elif filter_type == 'highpass':
            self.highpass_frame.pack(fill=tk.X, pady=5)
        elif filter_type == 'bandpass':
            self.bandpass_frame.pack(fill=tk.X, pady=5)

    def validate_inputs(self):
        """Valideaza inputurile utilizatorului"""
        if not self.filter_type_var.get():
            messagebox.showerror("Eroare", "Selecteaza un tip de filtru!")
            return False

        fs = self.sampling_freq_var.get()
        nyquist = fs / 2

        filter_type = self.filter_type_var.get()

        if filter_type == 'lowpass':
            cutoff = self.lowpass_cutoff_var.get()
            if cutoff >= nyquist:
                messagebox.showerror("Eroare",
                    f"Frecventa de taiere ({cutoff} Hz) trebuie sa fie mai mica decat frecventa Nyquist ({nyquist} Hz)!")
                return False

        elif filter_type == 'highpass':
            cutoff = self.highpass_cutoff_var.get()
            if cutoff >= nyquist:
                messagebox.showerror("Eroare",
                    f"Frecventa de taiere ({cutoff} Hz) trebuie sa fie mai mica decat frecventa Nyquist ({nyquist} Hz)!")
                return False

        elif filter_type == 'bandpass':
            low = self.bandpass_low_var.get()
            high = self.bandpass_high_var.get()

            if low >= high:
                messagebox.showerror("Eroare",
                    "Frecventa inferioara trebuie sa fie mai mica decat frecventa superioara!")
                return False

            if high >= nyquist:
                messagebox.showerror("Eroare",
                    f"Frecventa superioara ({high} Hz) trebuie sa fie mai mica decat frecventa Nyquist ({nyquist} Hz)!")
                return False

        return True

    def apply_filter(self):
        """Handler pentru butonul Aplica"""
        if not self.validate_inputs():
            return

        self.selected_filter = self.filter_type_var.get()

        # Colecteaza parametrii
        self.filter_params = {
            'filter_type': self.selected_filter,
            'order': self.order_var.get(),
            'sampling_freq': self.sampling_freq_var.get(),
        }

        if self.selected_filter == 'lowpass':
            self.filter_params['cutoff'] = self.lowpass_cutoff_var.get()
        elif self.selected_filter == 'highpass':
            self.filter_params['cutoff'] = self.highpass_cutoff_var.get()
        elif self.selected_filter == 'bandpass':
            self.filter_params['low_cutoff'] = self.bandpass_low_var.get()
            self.filter_params['high_cutoff'] = self.bandpass_high_var.get()

        self.root.destroy()

    def cancel(self):
        """Handler pentru butonul Anuleaza"""
        self.selected_filter = None
        self.root.destroy()

    def run(self):
        """Ruleaza interfata grafica"""
        self.root.mainloop()
        return self.selected_filter, self.filter_params


def get_filter_configuration():
    """
    Afiseaza GUI si returneaza configuratia aleasa

    Returns:
    --------
    tuple : (filter_type, params_dict) sau (None, {})
    """
    gui = FilterGUI()
    return gui.run()