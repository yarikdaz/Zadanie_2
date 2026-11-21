# Prevodník teploty °C → °F

Jednoduchá desktopová aplikácia v Pythone, ktorá generuje pole náhodných teplôt, vykonáva s ním základné operácie, prepočítava hodnoty podľa vzorca a zobrazuje pôvodné aj vypočítané hodnoty v jednom grafe.

## Funkcie

- **Pole vstupných hodnôt** – 50 náhodných teplôt v °C (rozsah −10 až 40 °C).
- **Operácie s poľom** – priemer, medián, minimum, maximum a zoradenie od najmenšej po najväčšiu hodnotu.
- **Výpočet** – prevod stupňov Celzia na stupne Fahrenheita:

  `F = C × 9/5 + 32`

- **Graf** – pôvodné (°C) aj vypočítané (°F) hodnoty v jednom grafe na porovnanie.
- **Vlastný výpočet** – po zadaní ľubovoľného čísla do vstupného poľa aplikácia vypočíta jeho hodnotu vo °F (podporuje aj desatinnú čiarku, napr. `21,5`).

## Ovládanie

| Prvok | Popis |
|---|---|
| Vstupné pole | Zadajte teplotu v °C |
| **Vypočítať** | Prepočíta zadané číslo na °F (alebo stlačte Enter) |
| **Nové náhodné hodnoty** | Vygeneruje nové pole 50 hodnôt a prekreslí graf |
| **Zoradiť / pôvodné poradie** | Prepína medzi zoradeným a pôvodným poradím hodnôt |

## Spustenie

### Variant A – hotový .exe súbor (bez Pythonu)

Spustite `PrevodnikTeploty.exe` z priečinka `dist`. Python nie je potrebný.

### Variant B – zo zdrojového kódu

Požiadavky: Python 3.9+ (tkinter je súčasťou štandardnej inštalácie).

```bash
pip install matplotlib
python aplikacia.py
```

## Vytvorenie .exe súboru

Na Windows stačí dvakrát kliknúť na `build_exe.bat`, alebo spustiť ručne:

```bash
pip install pyinstaller matplotlib
pyinstaller --onefile --windowed --name PrevodnikTeploty aplikacia.py
```

Výsledný súbor nájdete v `dist\PrevodnikTeploty.exe`.

> **Poznámka:** Prvé spustenie .exe môže trvať niekoľko sekúnd, pretože sa súbor rozbaľuje. Antivírus môže pri súboroch z PyInstalleru zobraziť upozornenie – ide o falošný poplach.

## Štruktúra projektu

```
.
├── aplikacia.py     # zdrojový kód aplikácie
├── build_exe.bat    # skript na vytvorenie .exe
├── README.md        # tento súbor
└── dist/
    └── PrevodnikTeploty.exe   # vznikne po kompilácii
```

## Použité technológie

- Python 3
- tkinter (grafické rozhranie)
- matplotlib (graf)
- PyInstaller (kompilácia do .exe)
