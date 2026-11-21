"""
Aplikácia: Analýza nameraných hodnôt a prevod jednotiek
=======================================================
Splnenie zadania:
  1. Pole vstupných hodnôt  – min. 50 náhodných hodnôt (nastaviteľný počet 50 – 500)
  2. Práca s poľom          – zoradenie (vzostupne/zostupne), priemer, medián, min, max,
                              rozptyl, smerodajná odchýlka, rozsah, súčet
  3. Výpočet                – prevod podľa zvoleného vzorca (napr. F = C * 9/5 + 32)
  4. Graf a GUI             – pôvodné aj vypočítané hodnoty v jednom grafe, histogram,
                              tabuľka, vstupné pole, tlačidlá, popisy, história výpočtov
  5. Kompilácia do .exe     – pozri vytvor_exe.bat
"""
import csv
import random
import statistics
import tkinter as tk
from datetime import datetime
from tkinter import ttk, messagebox, filedialog

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

# ---------------------------------------------------------------------------
# Definícia veličín a prevodných vzorcov
# ---------------------------------------------------------------------------
VELICINY = {
    "Teplota": {
        "jednotka": "°C", "min": -10, "max": 35, "celociselne": False,
        "prevody": {
            "°F  (F = C · 9/5 + 32)": ("°F", lambda c: c * 9 / 5 + 32),
            "K  (K = C + 273,15)": ("K", lambda c: c + 273.15),
        },
    },
    "Tlak": {
        "jednotka": "hPa", "min": 950, "max": 1050, "celociselne": False,
        "prevody": {
            "kPa  (p / 10)": ("kPa", lambda p: p / 10),
            "mmHg  (p · 0,750062)": ("mmHg", lambda p: p * 0.750062),
            "psi  (p · 0,0145038)": ("psi", lambda p: p * 0.0145038),
        },
    },
    "Rýchlosť": {
        "jednotka": "km/h", "min": 0, "max": 130, "celociselne": False,
        "prevody": {
            "m/s  (v / 3,6)": ("m/s", lambda v: v / 3.6),
            "mph  (v · 0,621371)": ("mph", lambda v: v * 0.621371),
        },
    },
    "Počet zubov": {
        "jednotka": "ks", "min": 10, "max": 60, "celociselne": True,
        "prevody": {
            "Deliaci priemer d  (d = m · z, m = 2 mm)": ("mm", lambda z: 2 * z),
            "Obvod deliacej kružnice  (o = π · m · z)": ("mm", lambda z: 3.141592653589793 * 2 * z),
        },
    },
}

TMAVA = {"bg": "#1e1f26", "fg": "#e8e8e8"}


# ---------------------------------------------------------------------------
# Logika (nezávislá od GUI)
# ---------------------------------------------------------------------------
def generuj_hodnoty(n, minimum, maximum, celociselne, seed=None):
    """Vygeneruje pole náhodných hodnôt."""
    rnd = random.Random(seed)
    if celociselne:
        return [rnd.randint(int(minimum), int(maximum)) for _ in range(n)]
    return [round(rnd.uniform(minimum, maximum), 1) for _ in range(n)]


def zorad(hodnoty, rezim):
    if rezim == "Vzostupne":
        return sorted(hodnoty)
    if rezim == "Zostupne":
        return sorted(hodnoty, reverse=True)
    return list(hodnoty)


def statistiky(hodnoty):
    """Vráti slovník štatistických ukazovateľov poľa."""
    return {
        "Počet": len(hodnoty),
        "Súčet": sum(hodnoty),
        "Priemer": statistics.mean(hodnoty),
        "Medián": statistics.median(hodnoty),
        "Minimum": min(hodnoty),
        "Maximum": max(hodnoty),
        "Rozsah": max(hodnoty) - min(hodnoty),
        "Rozptyl": statistics.pvariance(hodnoty),
        "Smerodajná odchýlka": statistics.pstdev(hodnoty),
    }


# ---------------------------------------------------------------------------
# GUI
# ---------------------------------------------------------------------------
class Aplikacia:
    def __init__(self, root):
        self.root = root
        root.title("Analýza meraných hodnôt a prevod jednotiek")
        root.geometry("1180x780")
        root.minsize(1000, 680)

        self.povodne = []          # pôvodné (negenerované znova) hodnoty
        self.historia = []         # história jednotlivých výpočtov

        self._vytvor_menu()
        self._vytvor_premenne()
        self._vytvor_rozlozenie()
        self.generuj()

    # ----------------------------- menu ----------------------------------
    def _vytvor_menu(self):
        menu = tk.Menu(self.root)
        subor = tk.Menu(menu, tearoff=0)
        subor.add_command(label="Exportovať do CSV…", command=self.export_csv)
        subor.add_command(label="Uložiť graf ako PNG…", command=self.uloz_graf)
        subor.add_separator()
        subor.add_command(label="Koniec", command=self.root.destroy)
        menu.add_cascade(label="Súbor", menu=subor)

        pomoc = tk.Menu(menu, tearoff=0)
        pomoc.add_command(label="O aplikácii", command=self.o_aplikacii)
        menu.add_cascade(label="Pomocník", menu=pomoc)
        self.root.config(menu=menu)

    def o_aplikacii(self):
        messagebox.showinfo(
            "O aplikácii",
            "Analýza meraných hodnôt a prevod jednotiek\n\n"
            "• generovanie náhodných hodnôt\n"
            "• štatistika a zoradenie poľa\n"
            "• prevod podľa zvoleného vzorca\n"
            "• porovnanie v grafe, histogram, tabuľka\n"
            "• export do CSV a PNG\n\nVytvorené v Pythone (tkinter + matplotlib).")

    # --------------------------- premenné --------------------------------
    def _vytvor_premenne(self):
        self.var_velicina = tk.StringVar(value="Teplota")
        self.var_prevod = tk.StringVar()
        self.var_pocet = tk.IntVar(value=60)
        self.var_min = tk.StringVar()
        self.var_max = tk.StringVar()
        self.var_seed = tk.StringVar(value="")
        self.var_zorad = tk.StringVar(value="Pôvodné poradie")
        self.var_typ = tk.StringVar(value="Čiarový")
        self.var_ukaz_pov = tk.BooleanVar(value=True)
        self.var_ukaz_vyp = tk.BooleanVar(value=True)
        self.var_ukaz_priemer = tk.BooleanVar(value=True)
        self.var_ukaz_mriezku = tk.BooleanVar(value=True)
        self.var_vstup = tk.StringVar()
        self.var_stav = tk.StringVar(value="Pripravené.")

    # --------------------------- rozloženie ------------------------------
    def _vytvor_rozlozenie(self):
        hlavny = ttk.Frame(self.root, padding=8)
        hlavny.pack(fill=tk.BOTH, expand=True)

        # ---- ľavý panel: nastavenia + kalkulačka ----
        lavy = ttk.Frame(hlavny)
        lavy.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 8))

        # Nastavenia
        nast = ttk.LabelFrame(lavy, text=" 1. Vstupné hodnoty ", padding=8)
        nast.pack(fill=tk.X)

        ttk.Label(nast, text="Veličina:").grid(row=0, column=0, sticky="w", pady=2)
        cb_vel = ttk.Combobox(nast, textvariable=self.var_velicina, state="readonly",
                              values=list(VELICINY.keys()), width=22)
        cb_vel.grid(row=0, column=1, sticky="ew", pady=2)
        cb_vel.bind("<<ComboboxSelected>>", lambda e: self.zmena_velicinu())

        ttk.Label(nast, text="Počet hodnôt (50–500):").grid(row=1, column=0, sticky="w", pady=2)
        ttk.Spinbox(nast, from_=50, to=500, textvariable=self.var_pocet, width=8).grid(
            row=1, column=1, sticky="w", pady=2)

        ttk.Label(nast, text="Minimum:").grid(row=2, column=0, sticky="w", pady=2)
        ttk.Entry(nast, textvariable=self.var_min, width=10).grid(row=2, column=1, sticky="w", pady=2)

        ttk.Label(nast, text="Maximum:").grid(row=3, column=0, sticky="w", pady=2)
        ttk.Entry(nast, textvariable=self.var_max, width=10).grid(row=3, column=1, sticky="w", pady=2)

        ttk.Label(nast, text="Seed (voliteľné):").grid(row=4, column=0, sticky="w", pady=2)
        ttk.Entry(nast, textvariable=self.var_seed, width=10).grid(row=4, column=1, sticky="w", pady=2)

        ttk.Button(nast, text="⟳  Generovať nové hodnoty", command=self.generuj).grid(
            row=5, column=0, columnspan=2, sticky="ew", pady=(8, 0))
        nast.columnconfigure(1, weight=1)

        # Spracovanie
        spr = ttk.LabelFrame(lavy, text=" 2. Spracovanie a výpočet ", padding=8)
        spr.pack(fill=tk.X, pady=(8, 0))

        ttk.Label(spr, text="Vzorec prevodu:").grid(row=0, column=0, sticky="w", pady=2)
        self.cb_prevod = ttk.Combobox(spr, textvariable=self.var_prevod, state="readonly", width=34)
        self.cb_prevod.grid(row=1, column=0, sticky="ew", pady=2)
        self.cb_prevod.bind("<<ComboboxSelected>>", lambda e: self.prekresli())

        ttk.Label(spr, text="Zoradenie:").grid(row=2, column=0, sticky="w", pady=(6, 2))
        cb_z = ttk.Combobox(spr, textvariable=self.var_zorad, state="readonly", width=34,
                            values=["Pôvodné poradie", "Vzostupne", "Zostupne"])
        cb_z.grid(row=3, column=0, sticky="ew", pady=2)
        cb_z.bind("<<ComboboxSelected>>", lambda e: self.prekresli())
        spr.columnconfigure(0, weight=1)

        # Zobrazenie
        zob = ttk.LabelFrame(lavy, text=" 3. Zobrazenie grafu ", padding=8)
        zob.pack(fill=tk.X, pady=(8, 0))
        ttk.Label(zob, text="Typ grafu:").grid(row=0, column=0, sticky="w")
        cb_t = ttk.Combobox(zob, textvariable=self.var_typ, state="readonly", width=12,
                            values=["Čiarový", "Bodový"])
        cb_t.grid(row=0, column=1, sticky="w", padx=4)
        cb_t.bind("<<ComboboxSelected>>", lambda e: self.prekresli())
        for i, (txt, var) in enumerate([("Pôvodné hodnoty", self.var_ukaz_pov),
                                        ("Vypočítané hodnoty", self.var_ukaz_vyp),
                                        ("Priemer (pôvodné)", self.var_ukaz_priemer),
                                        ("Mriežka", self.var_ukaz_mriezku)], start=1):
            ttk.Checkbutton(zob, text=txt, variable=var, command=self.prekresli).grid(
                row=i, column=0, columnspan=2, sticky="w")

        # Kalkulačka
        kal = ttk.LabelFrame(lavy, text=" 4. Prevod ľubovoľného čísla ", padding=8)
        kal.pack(fill=tk.BOTH, expand=True, pady=(8, 0))

        self.lbl_vstup = ttk.Label(kal, text="Zadajte hodnotu:")
        self.lbl_vstup.grid(row=0, column=0, sticky="w")
        self.ent_vstup = ttk.Entry(kal, textvariable=self.var_vstup, width=14)
        self.ent_vstup.grid(row=0, column=1, sticky="w", padx=4)
        self.ent_vstup.bind("<Return>", lambda e: self.vypocitaj())
        ttk.Button(kal, text="Vypočítať", command=self.vypocitaj).grid(row=0, column=2, padx=2)

        self.lbl_vysledok = ttk.Label(kal, text="Výsledok: –", font=("Segoe UI", 11, "bold"),
                                      foreground="#0b6e4f")
        self.lbl_vysledok.grid(row=1, column=0, columnspan=3, sticky="w", pady=6)

        ttk.Label(kal, text="História výpočtov:").grid(row=2, column=0, columnspan=3, sticky="w")
        self.lst_hist = tk.Listbox(kal, height=5)
        self.lst_hist.grid(row=3, column=0, columnspan=3, sticky="nsew")
        ttk.Button(kal, text="Vymazať históriu", command=self.vymaz_historiu).grid(
            row=4, column=0, columnspan=3, sticky="ew", pady=(4, 0))
        kal.rowconfigure(3, weight=1)
        kal.columnconfigure(1, weight=1)

        # ---- pravý panel: záložky ----
        pravy = ttk.Frame(hlavny)
        pravy.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.notebook = ttk.Notebook(pravy)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # záložka Graf
        tab_graf = ttk.Frame(self.notebook)
        self.notebook.add(tab_graf, text="  Graf porovnania  ")
        self.fig1 = Figure(figsize=(7, 4.6), dpi=100)
        self.ax1 = self.fig1.add_subplot(111)
        self.ax2 = self.ax1.twinx()
        self.canvas1 = FigureCanvasTkAgg(self.fig1, master=tab_graf)
        NavigationToolbar2Tk(self.canvas1, tab_graf).update()
        self.canvas1.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # záložka Histogram
        tab_hist = ttk.Frame(self.notebook)
        self.notebook.add(tab_hist, text="  Histogram  ")
        self.fig2 = Figure(figsize=(7, 4.6), dpi=100)
        self.canvas2 = FigureCanvasTkAgg(self.fig2, master=tab_hist)
        self.canvas2.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # záložka Tabuľka
        tab_tab = ttk.Frame(self.notebook)
        self.notebook.add(tab_tab, text="  Tabuľka hodnôt  ")
        self.tree = ttk.Treeview(tab_tab, columns=("i", "pov", "vyp"), show="headings")
        sb = ttk.Scrollbar(tab_tab, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sb.pack(side=tk.RIGHT, fill=tk.Y)

        # záložka Štatistika
        tab_st = ttk.Frame(self.notebook)
        self.notebook.add(tab_st, text="  Štatistika  ")
        self.tree_st = ttk.Treeview(tab_st, columns=("n", "pov", "vyp"), show="headings", height=12)
        self.tree_st.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # stavový riadok
        ttk.Label(self.root, textvariable=self.var_stav, relief=tk.SUNKEN, anchor="w",
                  padding=(6, 2)).pack(side=tk.BOTTOM, fill=tk.X)

    # --------------------------- akcie -----------------------------------
    def zmena_velicinu(self):
        v = VELICINY[self.var_velicina.get()]
        self.var_min.set(str(v["min"]))
        self.var_max.set(str(v["max"]))
        nazvy = list(v["prevody"].keys())
        self.cb_prevod.config(values=nazvy)
        self.var_prevod.set(nazvy[0])
        self.lbl_vstup.config(text=f"Zadajte hodnotu [{v['jednotka']}]:")
        self.vymaz_historiu()
        self.lbl_vysledok.config(text="Výsledok: –")
        self.generuj()

    def aktualny_prevod(self):
        v = VELICINY[self.var_velicina.get()]
        if self.var_prevod.get() not in v["prevody"]:
            self.var_prevod.set(list(v["prevody"].keys())[0])
        return v["prevody"][self.var_prevod.get()]  # (jednotka, funkcia)

    def generuj(self):
        v = VELICINY[self.var_velicina.get()]
        if not self.var_min.get() or not self.var_max.get():
            self.var_min.set(str(v["min"]))
            self.var_max.set(str(v["max"]))
            self.cb_prevod.config(values=list(v["prevody"].keys()))
            if not self.var_prevod.get():
                self.var_prevod.set(list(v["prevody"].keys())[0])
        try:
            n = int(self.var_pocet.get())
            mn = float(self.var_min.get().replace(",", "."))
            mx = float(self.var_max.get().replace(",", "."))
            if not 50 <= n <= 500:
                raise ValueError("Počet hodnôt musí byť v rozsahu 50 až 500.")
            if mn >= mx:
                raise ValueError("Minimum musí byť menšie ako maximum.")
            seed = self.var_seed.get().strip()
            seed = int(seed) if seed else None
        except (ValueError, tk.TclError) as e:
            messagebox.showerror("Neplatný vstup", str(e) if str(e) and "invalid literal" not in str(e)
                                 and "could not convert" not in str(e)
                                 else "Skontrolujte počet, minimum, maximum a seed (celé číslo).")
            return
        self.povodne = generuj_hodnoty(n, mn, mx, v["celociselne"], seed)
        self.var_stav.set(f"Vygenerovaných {n} hodnôt ({self.var_velicina.get()}, "
                          f"{mn:g} – {mx:g} {v['jednotka']}) – {datetime.now():%H:%M:%S}")
        self.prekresli()

    def vypocitaj(self):
        v = VELICINY[self.var_velicina.get()]
        jednotka2, funkcia = self.aktualny_prevod()
        text = self.var_vstup.get().replace(",", ".").strip()
        try:
            x = float(text)
        except ValueError:
            messagebox.showerror("Chyba", "Zadajte platné číslo (napr. 21.5).")
            return
        y = funkcia(x)
        riadok = f"{x:g} {v['jednotka']}  →  {y:.3f} {jednotka2}"
        self.lbl_vysledok.config(text=f"Výsledok: {riadok}")
        self.lst_hist.insert(0, f"{datetime.now():%H:%M:%S}   {riadok}")
        self.var_stav.set("Výpočet vykonaný.")

    def vymaz_historiu(self):
        self.lst_hist.delete(0, tk.END)

    # --------------------------- vykresľovanie ---------------------------
    def prekresli(self):
        if not self.povodne:
            return
        v = VELICINY[self.var_velicina.get()]
        j1 = v["jednotka"]
        j2, funkcia = self.aktualny_prevod()

        hodnoty = zorad(self.povodne, self.var_zorad.get())
        vypocitane = [funkcia(h) for h in hodnoty]
        x = list(range(1, len(hodnoty) + 1))

        self._graf_porovnanie(x, hodnoty, vypocitane, j1, j2)
        self._histogram(hodnoty, vypocitane, j1, j2)
        self._tabulka(hodnoty, vypocitane, j1, j2)
        self._statistika(hodnoty, vypocitane, j1, j2)

    def _graf_porovnanie(self, x, hodnoty, vypocitane, j1, j2):
        self.ax1.clear()
        self.ax2.clear()
        styl_pov, styl_vyp = ("o-", "s--") if self.var_typ.get() == "Čiarový" else ("o", "s")
        handles = []
        if self.var_ukaz_pov.get():
            h, = self.ax1.plot(x, hodnoty, styl_pov, color="tab:blue", markersize=4,
                               label=f"Pôvodné ({j1})")
            handles.append(h)
        if self.var_ukaz_vyp.get():
            h, = self.ax2.plot(x, vypocitane, styl_vyp, color="tab:red", markersize=4,
                               label=f"Vypočítané ({j2})")
            handles.append(h)
        if self.var_ukaz_priemer.get() and self.var_ukaz_pov.get():
            pr = statistics.mean(hodnoty)
            h = self.ax1.axhline(pr, color="tab:green", linestyle=":", linewidth=1.8,
                                 label=f"Priemer = {pr:.2f} {j1}")
            handles.append(h)
        self.ax1.set_xlabel("Poradie merania")
        self.ax1.set_ylabel(f"Pôvodné hodnoty [{j1}]", color="tab:blue")
        self.ax2.set_ylabel(f"Vypočítané hodnoty [{j2}]", color="tab:red")
        self.ax1.set_title(f"{self.var_velicina.get()}: porovnanie pôvodných a vypočítaných hodnôt")
        self.ax1.grid(self.var_ukaz_mriezku.get(), alpha=0.3)
        if handles:
            self.ax1.legend(handles=handles, loc="best", fontsize=9)
        self.fig1.tight_layout()
        self.canvas1.draw()

    def _histogram(self, hodnoty, vypocitane, j1, j2):
        self.fig2.clear()
        a = self.fig2.add_subplot(121)
        b = self.fig2.add_subplot(122)
        bins = min(15, max(5, len(hodnoty) // 5))
        a.hist(hodnoty, bins=bins, color="tab:blue", edgecolor="white")
        a.axvline(statistics.mean(hodnoty), color="tab:green", linestyle="--", label="priemer")
        a.set_title(f"Pôvodné [{j1}]")
        a.set_xlabel(j1); a.set_ylabel("Početnosť"); a.legend()
        b.hist(vypocitane, bins=bins, color="tab:red", edgecolor="white")
        b.axvline(statistics.mean(vypocitane), color="tab:green", linestyle="--", label="priemer")
        b.set_title(f"Vypočítané [{j2}]")
        b.set_xlabel(j2); b.legend()
        self.fig2.tight_layout()
        self.canvas2.draw()

    def _tabulka(self, hodnoty, vypocitane, j1, j2):
        self.tree.heading("i", text="#")
        self.tree.heading("pov", text=f"Pôvodná hodnota [{j1}]")
        self.tree.heading("vyp", text=f"Vypočítaná hodnota [{j2}]")
        self.tree.column("i", width=60, anchor="center")
        self.tree.column("pov", width=200, anchor="center")
        self.tree.column("vyp", width=200, anchor="center")
        self.tree.delete(*self.tree.get_children())
        for i, (p, v) in enumerate(zip(hodnoty, vypocitane), start=1):
            self.tree.insert("", tk.END, values=(i, f"{p:g}", f"{v:.3f}"))

    def _statistika(self, hodnoty, vypocitane, j1, j2):
        self.tree_st.heading("n", text="Ukazovateľ")
        self.tree_st.heading("pov", text=f"Pôvodné [{j1}]")
        self.tree_st.heading("vyp", text=f"Vypočítané [{j2}]")
        self.tree_st.column("n", width=200, anchor="w")
        self.tree_st.column("pov", width=170, anchor="center")
        self.tree_st.column("vyp", width=170, anchor="center")
        self.tree_st.delete(*self.tree_st.get_children())
        s1, s2 = statistiky(hodnoty), statistiky(vypocitane)
        for k in s1:
            if k == "Počet":
                self.tree_st.insert("", tk.END, values=(k, s1[k], s2[k]))
            else:
                self.tree_st.insert("", tk.END, values=(k, f"{s1[k]:.3f}", f"{s2[k]:.3f}"))

    # --------------------------- export ----------------------------------
    def export_csv(self):
        if not self.povodne:
            return
        cesta = filedialog.asksaveasfilename(defaultextension=".csv",
                                             filetypes=[("CSV súbor", "*.csv")])
        if not cesta:
            return
        v = VELICINY[self.var_velicina.get()]
        j2, f = self.aktualny_prevod()
        hodnoty = zorad(self.povodne, self.var_zorad.get())
        try:
            with open(cesta, "w", newline="", encoding="utf-8-sig") as fh:
                w = csv.writer(fh, delimiter=";")
                w.writerow(["Poradie", f"Povodne [{v['jednotka']}]", f"Vypocitane [{j2}]"])
                for i, h in enumerate(hodnoty, start=1):
                    w.writerow([i, h, round(f(h), 3)])
            self.var_stav.set(f"Exportované do: {cesta}")
        except OSError as e:
            messagebox.showerror("Chyba exportu", str(e))

    def uloz_graf(self):
        cesta = filedialog.asksaveasfilename(defaultextension=".png",
                                             filetypes=[("Obrázok PNG", "*.png")])
        if not cesta:
            return
        try:
            self.fig1.savefig(cesta, dpi=150)
            self.var_stav.set(f"Graf uložený: {cesta}")
        except OSError as e:
            messagebox.showerror("Chyba uloženia", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    try:
        ttk.Style().theme_use("vista")
    except tk.TclError:
        pass
    app = Aplikacia(root)
    app.zmena_velicinu()
    root.mainloop()
