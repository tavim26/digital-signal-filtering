# Filtrare Semnale Digitale

Implementare filtre digitale: trece-jos, trece-sus si trece-banda pentru procesarea semnalelor din fisiere CSV sau Excel.

## Descriere

Proiect pentru procesarea semnalelor digitale folosind trei tipuri de filtre:
- Filtru trece-jos (Low-pass) - elimina frecventele inalte
- Filtru trece-sus (High-pass) - elimina frecventele joase  
- Filtru trece-banda (Band-pass) - pastreaza doar o banda de frecvente

## Cerinte sistem

- Python 3.10 sau mai recent
- Git instalat
- PyCharm 

## Instalare si setup 

### Pasul 1: Cloneaza repository-ul

Deschide terminal/cmd si navigheaza unde vrei sa salvezi proiectul:
```bash
cd C:\Users\[username]\Desktop
git clone https://github.com/[username]/Filtrare-Semnale-Digitale.git
cd Filtrare-Semnale-Digitale
```

### Pasul 2: Deschide proiectul in PyCharm

1. Deschide PyCharm
2. File → Open
3. Selecteaza directorul `Filtrare-Semnale-Digitale`
4. Click OK

### Pasul 3: Configureaza mediul virtual Python

**IMPORTANT:** Fiecare dezvoltator trebuie sa isi creeze propriul mediu virtual local.

#### Configurare venv din terminal

In terminal PyCharm (View → Tool Windows → Terminal):
```bash
# Windows
python -m venv venv
venv\Scripts\activate
```

### Pasul 4: Instaleaza dependentele

Cu mediul virtual activ, in terminal PyCharm:
```bash
pip install -r requirements.txt
```

Astepti sa se instaleze toate bibliotecile (numpy, scipy, pandas, matplotlib, etc.)

### Pasul 5: Verifica instalarea

Ruleaza in terminal:
```bash
python -c "import numpy, scipy, pandas, matplotlib; print('Toate bibliotecile sunt instalate corect!')"
```

Daca apare mesajul de succes, totul este OK.

### Pasul 6: Testeaza proiectul
```bash
python src/main.py
```

Daca nu exista erori de import, setup-ul este complet.

## Structura proiect
```
Filtrare-Semnale-Digitale/
├── data/
│   ├── raw/              # Pune aici fisierele CSV/Excel de intrare
│   └── processed/        # Aici se salveaza rezultatele filtrate
├── src/
│   ├── data_loader.py    # Functii pentru citirea datelor
│   ├── filters.py        # Implementare filtre digitale
│   ├── visualization.py  # Functii pentru grafice
│   └── main.py           # Script principal
├── docs/                 # Documentatie
├── requirements.txt      # Lista biblioteci necesare
├── config.py             # Configurari globale
└── .gitignore            # Fisiere ignorate de Git
```

## Utilizare

### Adauga date de intrare

1. Copiaza fisierul tau CSV sau Excel in `data/raw/`
2. Fisierul trebuie sa contina doua coloane:
   - Coloana 1: timp (sau index)
   - Coloana 2: valori semnal

### Ruleaza filtrarea
```bash
python src/main.py
```

Rezultatele filtrate se vor salva in `data/processed/`

## Workflow Git pentru colaborare

### Inainte sa incepi sa lucrezi

Asigura-te ca ai ultima versiune:
```bash
git pull origin main
```

### Dupa ce faci modificari

1. Verifica ce ai modificat:
```bash
git status
```

2. Adauga fisierele modificate:
```bash
git add .
```

3. Commit cu mesaj descriptiv:
```bash
git commit -m "mesaj"
```

4. Trimite pe GitHub:
```bash
git push origin main
```
