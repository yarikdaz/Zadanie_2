# Analýza meraných hodnôt a prevod jednotiek

Desktopová aplikácia v Pythone (tkinter + matplotlib), ktorá vygeneruje pole náhodných hodnôt, spracuje ich, prepočíta podľa zvoleného vzorca a zobrazí pôvodné aj vypočítané hodnoty v jednom grafe. Aplikáciu je možné skompilovať do `.exe` súboru a spúšťať ju aj na počítači bez nainštalovaného Pythonu.

## Obsah projektu

| Súbor | Popis |
|---|---|
| `aplikacia.py` | Zdrojový kód aplikácie |
| `vytvor_exe.bat` | Skript na vytvorenie `.exe` súboru (Windows) |
| `README.md` | Tento dokument |

## Plnenie zadania

| Bod zadania | Realizácia |
|---|---|
| 1. Pole vstupných hodnôt | Generovanie 50 – 500 náhodných hodnôt (predvolene 60) v nastaviteľnom rozsahu, voliteľný `seed` pre opakovateľné výsledky |
| 2. Práca s poľom | Zoradenie (vzostupne / zostupne / pôvodné poradie), súčet, priemer, medián, minimum, maximum, rozsah, rozptyl, smerodajná odchýlka |
| 3. Výpočet | Prevod hodnôt podľa zvoleného vzorca (pozri nižšie) |
| 4. Graf a GUI | Jeden graf s pôvodnými aj vypočítanými hodnotami (dve osi Y), histogram, tabuľka, vstupné pole, popisy, tlačidlá, história výpočtov |
| 5. Kompilácia | `.exe` pomocou PyInstaller (`vytvor_exe.bat`) |

## Podporované veličiny a vzorce

| Veličina | Pôvodná jednotka | Dostupné vzorce |
|---|---|---|
| Teplota | °C | `F = C · 9/5 + 32`, `K = C + 273,15` |
| Tlak | hPa | `kPa = p / 10`, `mmHg = p · 0,750062`, `psi = p · 0,0145038` |
| Rýchlosť | km/h | `m/s = v / 3,6`, `mph = v · 0,621371` |
| Počet zubov | ks | Deliaci priemer `d = m · z`, obvod deliacej kružnice `o = π · m · z` (modul `m = 2 mm`) |

## Požiadavky

- Windows (pre `.exe`), Python 3.9 alebo novší
- Knižnice: `matplotlib` (tkinter je súčasťou štandardnej inštalácie Pythonu)
- Pri inštalácii Pythonu z [python.org](https://www.python.org/downloads/) zaškrtnite **„Add Python to PATH“**

## Spustenie zo zdrojového kódu

```bash
pip install matplotlib
python aplikacia.py
```

## Vytvorenie .exe súboru

### Automaticky

1. Uložte `aplikacia.py` a `vytvor_exe.bat` do jedného priečinka.
2. Spustite `vytvor_exe.bat` dvojitým kliknutím.
3. Hotový súbor nájdete v `dist\AnalyzaMeranychHodnot.exe`.

### Ručne

```bash
pip install matplotlib pyinstaller
pyinstaller --onefile --windowed --name AnalyzaMeranychHodnot aplikacia.py
```

Prepínače:
- `--onefile` – všetko sa zabalí do jedného `.exe`
- `--windowed` – po spustení sa neotvorí konzolové okno

Výsledný `.exe` je možné skopírovať na ľubovoľný počítač s Windows, Python nie je potrebný.

## Ovládanie aplikácie

1. **Vstupné hodnoty** – vyberte veličinu, počet hodnôt, minimum, maximum a prípadne `seed`, potom kliknite na **Generovať nové hodnoty**.
2. **Spracovanie a výpočet** – zvoľte vzorec prevodu a spôsob zoradenia.
3. **Zobrazenie grafu** – prepínajte typ grafu (čiarový / bodový) a zobrazenie pôvodných hodnôt, vypočítaných hodnôt, priemeru a mriežky.
4. **Prevod ľubovoľného čísla** – zadajte číslo do vstupného poľa a kliknite na **Vypočítať** (alebo stlačte Enter). Výsledok sa zobrazí pod poľom a uloží do histórie.
5. **Záložky** – *Graf porovnania*, *Histogram*, *Tabuľka hodnôt*, *Štatistika*.
6. **Menu Súbor** – export hodnôt do CSV (oddeľovač `;`, otvorí sa v Exceli) a uloženie grafu ako PNG.

## Riešenie problémov

- **`python` sa nenašlo** – preinštalujte Python so zaškrtnutou voľbou *Add Python to PATH*.
- **Antivírus blokuje `.exe`** – súbory vytvorené PyInstallerom občas spúšťajú falošné poplachy; pridajte súbor medzi výnimky.
- **Prvé spustenie `.exe` trvá niekoľko sekúnd** – je to normálne pri režime `--onefile` (súbory sa rozbaľujú do dočasného priečinka).
- **Zmena vzorca** – vzorce sú definované v slovníku `VELICINY` na začiatku súboru `aplikacia.py`; stačí pridať ďalší záznam.

## Použité technológie

- Python 3
- tkinter / ttk – grafické rozhranie
- matplotlib – grafy
- PyInstaller – vytvorenie `.exe`
