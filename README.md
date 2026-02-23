# OOP Game Simulator - Simulátor turnajů

## 📋 Obsah

1. [Přehled projektu](#přehled-projektu)
2. [Struktura projektu](#struktura-projektu)
3. [Architektura a struktura tříd](#architektura-a-struktura-tříd)
4. [Instalace a spuštění](#instalace-a-spuštění)
5. [Moduly a jejich popis](#moduly-a-jejich-popis)
6. [Datové struktury](#datové-struktury)
7. [Algoritmy](#algoritmy)
8. [Příklady použití](#příklady-použití)
9. [Optimalizace a standardy](#optimalizace-a-standardy)

---

## 🎯 Přehled projektu

**OOP Game Simulator** je Python aplikace pro simulaci turnajů mezi více hráči. Projekt demonstruje objektově orientované programování s využitím abstraktní dědičnosti, polimorfismu a Factory pattern.

### Hlavní funkce:
- ✅ Turnaje formou **Round-robin** (každý s každým)
- ✅ Turnaje formou **Eliminace** (vyřazovací systém/pavouk)
- ✅ **Abstraktní dědičnost** - `BaseTournament` jako základ
- ✅ **Factory pattern** - `TournamentFactory` pro vytváření turnajů
- ✅ **Polymorfismus** - jednotné rozhraní pro všechny typy turnajů
- ✅ Správné zpracování bye hráčů v eliminačních turnajích
- ✅ Prokládání nasazených a nenasazených hráčů
- ✅ Detailní záznamy zápasů a turnajů do JSON
- ✅ Komprehenzivní ošetření výjimek
- ✅ Dodržování PEP 8 standardů

---

## 📁 Struktura projektu

```
oop_game_simulator/
├── main.py              # Hlavní demonstrační program
├── game.py              # Základní herní třídy (Player, Match, Dice)
├── files.py             # Pomocné funkce pro práci se soubory
├── tournament.py        # Abstraktní turnajové třídy
├── tournament_test.py   # Automatizované testy turnajů
├── players.json         # Vstupní data hráčů
├── README.md            # Tento soubor
├── .venv/               # Virtuální prostředí Python
├── __pycache__/         # Cache Python modulů
├── diagrams/            # PlantUML diagramy architektury
└── images/              # Obrázky pro dokumentaci
```

**Klíčové soubory:**
- **main.py** - Vstupní bod aplikace, interaktivní menu pro výběr typu turnaje
- **game.py** - Herní engine (Player, Match, Dice, load_players)
- **files.py** - I/O operace (JSON, CSV, text)
- **tournament.py** - Turnajový systém s abstraktní dědičností
- **tournament_test.py** - Automatické testy všech funkcí
- **players.json** - Data 13 hráčů z různých zemí

---

## 🏗️ Architektura a struktura tříd

### Hierarchie tříd

```
Person (osoba s přezdívkou, pohlavím, datem narození)
  └── Player (hráč s stavem, zápasy, výhry, skóre)

Dice (statická třída pro hod kostkou)

Match (zápas mezi dvěma hráči)
  └── interactions with: Player, Dice

BaseTournament (abstraktní třída pro turnaje) - ABC
  ├── RoundRobinTournament (každý s každým)
  └── EliminationTournament (vyřazovací systém)

TournamentFactory (tovární třída pro vytváření turnajů)
TournamentPrinter (pomocná třída pro výstup)

Gender (Enum: male, female)
```

### Abstraktní dědičnost

**BaseTournament** je abstraktní třída definující rozhraní pro všechny turnaje:
- `play()` - abstraktní metoda (musí být implementována)
- `_print_tournament_header()` - společná metoda
- `print_standings()` - společná metoda
- `save_tournament_results()` - společná metoda

**RoundRobinTournament** a **EliminationTournament** implementují vlastní logiku `play()`.

### Factory Pattern

**TournamentFactory** poskytuje jednotný způsob vytváření turnajů:
```python
tournament = TournamentFactory.create(
    tournament_type="round_robin",  # nebo "elimination"
    players=players,
    location="Praha",
    winning_score=10,
    max_dice_value=6
)
```

### Detailní popis tříd

#### **Gender (Enum)**
```python
class Gender(Enum):
    male = 'man'
    female = 'woman'
```
Výčtový typ pro reprezentaci pohlaví osob.

#### **Dice (Simulátor kostky)**
```python
class Dice:
    @staticmethod
    def roll(max_value=6) -> int
```
- Generuje náhodné číslo v rozmezí 1 až `max_value`
- Validace: `max_value` musí být v rozmezí 4-9
- Vyvolá `ValueError` pokud je hodnota mimo povolený rozsah

#### **Person (Osoba)**
Základní třída pro reprezentaci osoby.

**Atributy:**
- `nickname: str` - přezdívka
- `_gender: Gender` - pohlaví
- `_birth: datetime` - čas vytvoření instance

**Metody:**
- `gender` (property) - přístup a validace pohlaví
- `get_seconds_from_birth() -> int` - počet sekund od vytvoření

#### **Player (Hráč)**
Dědí z `Person`, reprezentuje hráče s herními statistikami.

**Dodatečné atributy:**
- `state: str` - stav/zemi hráče
- `count_of_games: int` - počet odehraných zápasů
- `_wins: int` - počet výher (s validací)
- `score: Dict` - slovník se klíči 'plus' (body navíc) a 'minus' (body ubité)

**Dodatečné metody:**
- `wins` (property) - přístup k výhrám s validací
- `win_rate() -> float` - procento výher
- `overall_score() -> Tuple` - vrací (plus_body, minus_body)

#### **Match (Zápas)**
Reprezentuje zápas mezi dvěma hráči.

**Atributy:**
- `_hplayer: Player` - domácí hráč
- `_gplayer: Player` - hostující hráč
- `winning_score: int` - počet bodů k vítězství
- `max_dice_value: int` - maximální hodnota kostky
- `_datetime: datetime` - čas zahájení zápasu
- `hp_points: int` - aktuální body domácího
- `gp_points: int` - aktuální body hostujícího
- `_history: List[Tuple]` - historie skóre po každém kole

**Klíčové metody:**
- `play() -> None` - odehraje celý zápas
- `score() -> Tuple` - vrací aktuální skóre
- `get_history() -> List` - vrací historii vývoje skóre
- `save_match_results(filename) -> None` - uloží výsledky do JSON

**Privátní metody:**
- `__roll() -> int` - simuluje hod kostkou pro oba hráče

#### **BaseTournament (Abstraktní třída)**
Abstraktní základní třída pro všechny typy turnajů.

**Atributy:**
- `players: List[Player]` - seznam hráčů
- `location: str` - místo konání turnaje
- `winning_score: int` - body na zápas
- `max_dice_value: int` - maximální hodnota kostky
- `matches: List[Match]` - seznam odehraných zápasů
- `winner: Optional[Player]` - vítěz turnaje
- `_detailed_results: List[Dict]` - detailní záznamy

**Abstraktní metody:**
- `play() -> None` - musí implementovat každá podtřída

**Klíčové metody:**
- `get_standings() -> List[Tuple]` - vrací pořadí hráčů
- `print_standings() -> None` - vyprintuje tabulku
- `save_tournament_results(filename) -> None` - uloží detailní výsledky
- `_print_tournament_header() -> None` - vypíše hlavičku turnaje

#### **RoundRobinTournament**
Implementace turnaje "každý s každým".

**Specifické metody:**
- `play() -> None` - odehraje všechny zápasy v kolech
- `_generate_round_robin_schedule() -> List` - generuje rozpis kol
- `_determine_round_robin_winner() -> None` - určí vítěze

**Algoritmus:**
- N hráčů → N-1 kol
- Rotační algoritmus pro párování
- Lichý počet → jeden hráč má volný los (bye) v každém kole

#### **EliminationTournament**
Implementace vyřazovacího turnaje (pavouk).

**Specifické metody:**
- `play() -> None` - odehraje eliminační turnaj
- `_calculate_byes() -> int` - vypočítá počet bye hráčů
- `_get_elimination_round_name() -> str` - vrací název kola

**Algoritmus:**
- Vypočítá bye hráče (nasazené) na začátku
- Bye hráči automaticky postupují do dalšího kola
- Prokládání: nasazení hrají proti nenasazeným
- Pokračuje dokud nezbyde 1 vítěz

#### **TournamentFactory**
Tovární třída pro vytváření turnajů.

**Metody:**
- `create(tournament_type, players, location, ...) -> BaseTournament`
- `get_available_types() -> List[str]`

**Podporované typy:**
- `"round_robin"` - každý s každým
- `"elimination"` - vyřazovací systém

#### **TournamentPrinter**
Pomocná třída pro formátování výstupu.

**Statické metody:**
- `print_round_header(round_name)` - hlavička kola
- `print_match_info(p1, p2)` - info o zápase
- `print_match_result(...)` - výsledek zápasu
- `print_elimination_result(winner, loser)` - postup/vyřazení
- `print_bye_info(player)` - volný los
- `print_winner(winner_name)` - vítěz turnaje

---

## 🚀 Instalace a spuštění

### Požadavky
- Python 3.7+
- Standardní knihovny (json, csv, datetime, enum, random, abc, math)

### Instalace
```bash
# Klonování nebo stažení projektu
cd d:\ukoly\python\oop_game_simulator

# Žádné další závislosti se neinstalují (pouze stdlib)
```

### Spuštění

#### Interaktivní demo (hlavní program)
```bash
python main.py
```
Program zobrazí menu:
1. Každý s každým (Round-robin)
2. Eliminační systém (Pavouk)
3. Ukončit program

#### Automatické testy
```bash
python tournament_test.py
```
Spustí 4 testy:
- Round-robin turnaj (13 hráčů)
- Eliminační turnaj (13 hráčů)
- Test polymorfismu
- Test TournamentFactory

---

## 📦 Moduly a jejich popis

### **files.py**
Modul pro práci se soubory v různých formátech.

#### Funkce:

**`textfile_read(path, encoding='utf-8') -> str`**
- Načte obsah textového souboru
- Vyvolá `FileNotFoundError` pokud soubor neexistuje
- Vyvolá obecné výjimky pro ostatní chyby

**`textfile_write(path, data='', encoding='utf-8') -> None`**
- Uloží text do souboru
- Vytvoří soubor pokud neexistuje
- Vyvolá výjimky při chybě

**`jsonfile_read(path, encoding='utf-8') -> dict|list`**
- Načte a parsuje JSON soubor
- Vyvolá `FileNotFoundError` nebo `json.JSONDecodeError`

**`jsonfile_write(path, data=None, encoding='utf-8') -> None`**
- Uloží Python objekt jako JSON
- Výchozí `data = {}`
- Validuje vstup na `None`

**`csvfile_read(path, encoding='utf-8') -> list[dict]`**
- Načte CSV soubor se separátorem `;`
- Vrací seznam slovníků (řádky)
- Quotechar: `"`

**`csvfile_write(path, data=None, encoding='utf-8') -> None`**
- Uloží seznam slovníků do CSV
- Validace: data musí být neprázdný seznam slovníků
- Vyvolá `ValueError` pokud je seznam prázdný

### **game.py**
Jádro logiky her a hráčů.

#### Hlavní komponenty:
- `Gender` - enum pro pohlaví
- `Dice` - generátor náhodných hodů
- `Person` - základní třída pro osoby
- `Player` - třída hráče (dědí z Person)
- `Match` - třída pro jednotlivý zápas
- `load_players(json_file)` - funkce pro načtení hráčů

#### Schéma zápasu:
1. Inicializace: dva hráči, počet bodů na vítězství
2. Hrací smyčka: opakování hodů kostkou
3. Inkrementace bodů vítězného hráče v daném kole
4. Konec: když některý hráč dosáhne cílového skóre
5. Aktualizace statistik hráčů

### **tournament.py** 
Abstraktní turnajový systém s polymorfismem.

**Klíčové komponenty:**

1. **BaseTournament (ABC)** - abstraktní základní třída
   - Definuje společné rozhraní pro všechny turnaje
   - Abstraktní metoda `play()` - každá podtřída musí implementovat
   - Společné metody: `print_standings()`, `save_tournament_results()`

2. **RoundRobinTournament** - každý s každým
   - Rotační algoritmus pro generování kol
   - N hráčů → N-1 kol
   - Lichý počet: jeden hráč má volný los v každém kole
   - Vítěz: nejvíce výher, při rovnosti rozhoduje skóre

3. **EliminationTournament** - vyřazovací systém
   - Vypočítá bye hráče (nasazené) pomocí `_calculate_byes()`
   - Bye hráči postupují přímo do dalšího kola
   - Prokládání: nasazení hrají proti nenasazeným
   - Správná struktura pavouka pro libovolný počet hráčů
   - Příklad: 13 hráčů → 3 bye + 10 hraje → 8 čtvrtfinále → 4 semifinále → 2 finále

4. **TournamentFactory** - tovární třída
   - Vytváří instance turnajů podle typu
   - `create(tournament_type, ...)` - hlavní metoda
   - `get_available_types()` - seznam podporovaných typů
   - Vyvolá `ValueError` pro neznámý typ

5. **TournamentPrinter** - formátování výstupu
   - Statické metody pro tisk
   - Hlavičky kol, výsledků zápasů, tabulky
   - ASCII art separátory

#### Algoritmus Round-robin:
Generuje rozpis kol tak, aby každý hráč hrál v každém kole max. jednou:
- Pro n hráčů se vytvoří n-1 kol
- Při lichém počtu jeden hráč má v daném kole "volno" (BYE)
- Algoritmus rotace: první hráč zůstává, ostatní rotují

#### Algoritmus Eliminace:
Vyřazovací systém s podporou lichého počtu hráčů:
- Vypočítá počet bye hráčů: `next_power_of_2 - num_players`
- Bye hráči automaticky postupují
- První kolo: nenasazení hrají mezi sebou
- Další kola: prokládání nasazených a nenasazených
- Pokračuje dokud zbývá 1 hráč (vítěz)

**Výpočet bye hráčů:**
```python
# Příklad: 13 hráčů
next_power = 16  # nejbližší mocnina 2
num_matches_first = 13 - 16//2 = 5  # zápasů v prvním kole
num_byes = 13 - (5 * 2) = 3  # bye hráčů
```

### **main.py**
Hlavní demonstrační program s interaktivním menu.

Plní funkce:
1. Zobrazí menu pro výběr typu turnaje
2. Načte hráče z `players.json`
3. Získá místo konání od uživatele
4. Vytvoří turnaj pomocí `TournamentFactory`
5. Odehraje turnaj a vypíše výsledky
6. Uloží výsledky do JSON souboru

### **tournament_test.py**
Automatizované testy pro ověření funkčnosti.

**4 testy:**
1. **Round-robin test** - 13 hráčů, 13 kol, 78 zápasů
2. **Eliminační test** - 13 hráčů, 3 bye, 12 zápasů
3. **Polymorfismus test** - vytvoření obou typů turnajů
4. **Factory test** - vytváření přes TournamentFactory, test neplatného typu

---

## 💾 Datové struktury

### **players.json** (Vstup)
```json
[
  {
    "nickname": "Jan",
    "gender": "man",
    "state": "CZ"
  },
  {
    "nickname": "Marie",
    "gender": "woman",
    "state": "SK"
  }
]
```

### **tournament_results.json** (Výstup - turnaj)
```json
{
  "tournament_info": {
    "date": "2026-02-23 22:30:00",
    "location": "Praha",
    "type": "round_robin",
    "winning_score": 10,
    "max_dice_value": 6,
    "num_players": 13
  },
  "players": [
    {"nickname": "Houska", "state": "CZE", "gender": "man"},
    {"nickname": "Jenny", "state": "CAN", "gender": "woman"}
  ],
  "winner": {
    "nickname": "Houska",
    "state": "CZE",
    "total_wins": 9,
    "total_games": 12,
    "win_rate": 75.0
  },
  "matches": [
    {
      "round": 1,
      "round_name": "KOLO 1",
      "match_type": "round_robin",
      "player1": {"nickname": "Houska", "state": "CZE"},
      "player2": {"nickname": "Jenny", "state": "CAN"},
      "final_score": {"player1": 10, "player2": 7},
      "winner": "Houska",
      "score_history": [[1,0], [2,0], [2,1]],
      "match_duration": 15
    }
  ],
  "final_standings": [
    {
      "position": 1,
      "player": "Houska",
      "state": "CZE",
      "wins": 9,
      "games": 12,
      "score_plus": 32,
      "score_minus": 20,
      "score_difference": 12,
      "win_rate": 75.0
    }
  ],
  "statistics": {
    "total_matches": 78,
    "total_rounds": 13,
    "average_match_duration": 15.33
  }
}
```

**Eliminační turnaj:**
```json
{
  "tournament_info": {
    "type": "elimination",
    "num_players": 13,
    "num_bye_players": 3
  },
  "matches": [
    {
      "round": 1,
      "round_name": "KOLO 13 HRÁČŮ",
      "match_type": "elimination",
      "player1": {"nickname": "Michelle"},
      "player2": {"nickname": "Justine"},
      "final_score": {"player1": 2, "player2": 3},
      "winner": "Justine",
      "eliminated": "Michelle"
    }
  ]
}
```

---

## 🔄 Algoritmy

### Round-robin Algoritmus (Generování kol)

```
1. Vstup: seznam hráčů (players)
2. n = počet hráčů
3. Pokud je n liché, přidej BYE (None)
4. Pro každé kolo (n-1 kol):
   a. Spáruj hráče: (players[0], players[n-1]), ..., (players[n/2-1], players[n/2])
   b. Vytvořené páry přidej do seznamu kola
   c. Vynech páry obsahující BYE
   d. Rotuj hráče: první zůstane, ostatní rotují cyklicky
5. Výstup: seznam kol (each kolo = seznam párů hráčů)
```

**Výhody:**
- Každý hráč hraje proti každému přesně jednou
- V každém kole hraje maximálně jednou
- Spravedlivé určení vítěze (nejvíce výher)

### Elimination Algoritmus (Vyřazovací systém)

```
1. Vstup: seznam hráčů (remaining_players)
2. Vypočítej bye hráče (nasazené):
   a. Najdi nejbližší vyšší mocninu 2
   b. num_byes = num_players - 2 * (num_players - next_power//2)
3. Bye hráči automaticky postupují do dalšího kola
4. První kolo: nenasazení hrají mezi sebou
5. Další kola: prokládat nasazené s nenasazenými
6. Dokud je více než 1 hráč:
   a. Spáruj sousední hráče (i, i+1)
   b. Pro každou páru:
      - Odehraj zápas
      - Vítěz postupuje do dalšího kola
      - Poražený je vyřazen
   c. Aktualizuj seznam hráčů na vítěze
7. Výstup: poslední zbylý hráč = vítěz
```

**Výpočet bye hráčů pro 13 hráčů:**
```
next_power = 16 (nejbližší mocnina 2)
matches_first_round = 13 - 16/2 = 5
num_byes = 13 - (5 * 2) = 3

Výsledek:
- 3 hráči mají volný los (bye)
- 10 hráčů hraje první kolo (5 zápasů)
- 8 hráčů postupuje do čtvrtfinále (5 vítězů + 3 bye)
- 4 do semifinále, 2 do finále
- Celkem: 12 zápasů (5+4+2+1)
```

**Prokládání hráčů:**
```python
# Bye hráči: [A, B, C]
# Vítězové prvního kola: [D, E, F, G, H]
# 
# Prokládání:
# [D, A, E, B, F, C, G, H]
#
# Páry ve čtvrtfinále:
# (D, A), (E, B), (F, C), (G, H)
# Nasazení A,B,C hrají proti nenasazeným D,E,F
```

**Charakteristika:**
- Počet kol: ⌈log₂(n)⌉
- Počet zápasů: n - 1
- Rychlejší než round-robin
- Tradiční systém (tenis, fotbal playoff)

---

## 💡 Příklady použití

### Příklad 1: Spuštění z příkazové řádky
```bash
# Interaktivní menu
python main.py

# Automatické testy
python tournament_test.py
```

### Příklad 2: Round-robin turnaj
```python
from game import load_players
from tournament import RoundRobinTournament

# Načti hráče
players = load_players("players.json")

# Vytvoř turnaj
tournament = RoundRobinTournament(
    players=players,
    location="Praha",
    winning_score=10,
    max_dice_value=6
)

# Odehraj a zobraz výsledky
tournament.play()
tournament.print_standings()

# Ulož výsledky
tournament.save_tournament_results("tournament_rr_praha.json")
```

### Příklad 3: Eliminační turnaj
```python
from tournament import EliminationTournament

# Vytvoř eliminační turnaj
tournament = EliminationTournament(
    players=players,
    location="Brno",
    winning_score=10,
    max_dice_value=6
)

tournament.play()
tournament.print_standings()
tournament.save_tournament_results("tournament_elim_brno.json")
```

### Příklad 4: Použití TournamentFactory
```python
from tournament import TournamentFactory

# Dostupné typy
types = TournamentFactory.get_available_types()
print(types)  # ['round_robin', 'elimination']

# Vytvoř turnaj pomocí Factory
tournament = TournamentFactory.create(
    tournament_type="round_robin",
    players=players,
    location="Praha",
    winning_score=10,
    max_dice_value=6
)

# Polymorfismus - stejné rozhraní pro oba typy
tournament.play()
tournament.print_standings()
```

### Příklad 5: Polymorfismus
```python
from tournament import BaseTournament, RoundRobinTournament, EliminationTournament

# Seznam různých typů turnajů
tournaments: list[BaseTournament] = [
    RoundRobinTournament(players, "Praha"),
    EliminationTournament(players, "Brno")
]

# Jednotné rozhraní
for tournament in tournaments:
    print(f"\n{tournament}")
    tournament.play()
    tournament.print_standings()
```

---

## 📊 Datové soubory

### Vstupy
- **players.json** - seznam hráčů (povinný pro `load_players()`)

### Výstupy (auto-generované)
- **tournament_rr_*.json** - výsledky round-robin turnajů
- **tournament_elim_*.json** - výsledky eliminačních turnajů

---

## ✅ Optimalizace a standardy

### PEP 8 Compliance
- ✅ Jména tříd: CamelCase (`Person`, `Match`, `BaseTournament`)
- ✅ Jména funkcí/metod: snake_case (`load_players`, `save_tournament_results`)
- ✅ Soukromé atributy: `_birth`, `_history` (single underscore)
- ✅ Dunder metody: `__init__`, `__str__`, `__roll` (private method)
- ✅ Max. linka 79 znaků pro kód, 72 pro komentáře
- ✅ Dvě prázdné řádky mezi třídami

### Google Style Docstrings
Všechny funkce a metody používají Google-style dokumentaci:
```python
"""Stručný popis.

Delší popis pokud je potřeba.

Args:
    param1 (type): Popis.
    param2 (type): Popis.

Returns:
    type: Popis vráceného.

Raises:
    ExceptionType: Popis situace.
"""
```

### Type Hints
Používání type hints pro lepší čitelnost:
```python
def load_players(json_file: str) -> List[Player]:
    ...

tournament: BaseTournament = TournamentFactory.create(
    tournament_type="round_robin",
    players=players,
    location="Praha"
)
```

### Abstract Base Classes (ABC)
Využití ABC modulu pro definici abstraktních tříd:
```python
from abc import ABC, abstractmethod

class BaseTournament(ABC):
    @abstractmethod
    def play(self) -> None:
        """Musí být implementováno v podtřídě."""
        pass
```

### Error Handling
- ✅ Vyvolávání specifických výjimek místo `print()`
- ✅ Kaskádované try-except bloky pro detail
- ✅ Jasné chybové zprávy s kontextem
- ✅ Validace vstupů na počátku funkcí

### Code Organization
- ✅ Moduly rozděleny dle funkce (files, game, tournament)
- ✅ Abstraktní třída jako základ hierarchie
- ✅ Factory pattern pro vytváření objektů
- ✅ Helper třída (TournamentPrinter) pro separaci výstupu
- ✅ `README.md` pro dokumentaci
- ✅ `main.py` jako entry point

---

## 🎓 Vzdělávací prvky

Projekt demonstruje:

1. **OOP Koncepty**
   - Abstraktní třída (`BaseTournament`)
   - Dědičnost (`RoundRobinTournament`, `EliminationTournament` → `BaseTournament`)
   - Polymorfismus (metody `play()`, různé implementace)
   - Zapouzdření (private atributy `_birth`, `_wins`)
   - Vlastnosti (properties `gender`, `wins`)

2. **Design Patterns**
   - **Abstract Base Class** - definice rozhraní
   - **Factory Pattern** - TournamentFactory
   - **Helper/Utility Class** - TournamentPrinter (statické metody)

3. **Python Specifika**
   - ABC modul (`@abstractmethod`)
   - Enum třídy (`Gender`)
   - Statické metody (`@staticmethod`)
   - List comprehensions
   - Type hints

4. **Algoritmy**
   - Round-robin scheduling (rotační algoritmus)
   - Elimination bracket (výpočet bye hráčů)
   - Prokládání hráčů v eliminaci

5. **Praktické dovednosti**
   - Práce se soubory (JSON)
   - Zpracování výjimek
   - Datové struktury (Dict, List, Tuple)
   - Formátování a tisk výstupů
   - Automatické testování

---

## 🚨 Známá omezení

1. **Lichý počet hráčů v Round-robin**: Jeden hráč má v každém kole "volno" (BYE)
2. **Losování v Eliminaci**: Pořadí hráčů není náhodně mícháno
3. **Bez persistentního DB**: Data se ukládají jen do JSON
4. **Bez GUI**: Pouze CLI interface

---

## 🔮 Možná rozšíření

Projekt je připraven pro rozšíření:
- ✨ Přidání dalších typů turnajů (Swiss system, Double elimination)
- ✨ Náhodné míchání hráčů před eliminačním turnajem
- ✨ Web interface
- ✨ Statistické analýzy a grafy
- ✨ Databázové úložiště
- ✨ Export do PDF/HTML

---

## 📄 Licencování

Projekt je pro vzdělávací účely.

---

**Poslední aktualizace:** 23. února 2026

1. **OOP Koncepty**
   - Dědičnost (`Player` → `Person`)
   - Polymorfismus (metody `play()`, `get_standings()`)
   - Zapouzdření (private atributy `_birth`, `_wins`)
   - Vlastnosti (properties `gender`, `wins`)

2. **Python Specifika**
   - Enum třídy (`Gender`, `TournamentType`)
   - Statické metody (`Dice.roll()`)
   - List comprehensions
   - Slicing a indexing seznamů

3. **Design Patterns**
   - Round-robin scheduling algoritmus
   - Vyřazovací systém (pavouk)
   - Builder pattern (vytváření turnaje)

4. **Praktické dovednosti**
   - Práce se soubory (textový, JSON, CSV)
   - Zpracování výjimek
   - Datové struktury (Dict, List, Tuple)
   - Formátování a tisk výstupů

---

## 📝 Změny a vývoj

### Verze 1.0 (Počáteční)
- Základní třídy `Person`, `Player`, `Dice`, `Match`
- Funkce pro práci se soubory
- Jednoduchý `main.py`

### Verze 2.0 (Turnaje)
- Třída `Tournament` s Round-robin a Elimination
- Generování rozpisu kol
- JSON export výsledků

---

## 🚨 Známá omezení

1. **Lichý počet hráčů v Round-robin**: Jeden hráč má v každém kole "volno" (BYE)
2. **Losování v Eliminaci**: Pořadí hráčů není mícháno (první si "vezme" druhého apod.)
3. **Bez persistentního DB**: Data se ukládají jen do JSON
4. **Bez GUI**: Pouze CLI interface

---

## 🤝 Příspěvky a úpravy

Projekt je připraven pro rozšíření:
- Přidání vlastních Enum typů
- Rozšíření dalších turnajových formátů
- Přidání persistentní databáze
- Web interface
- Statistické analýzy

---

## 📄 Licencování

Projekt je pro vzdělávací účely.

---

## 📞 Kontakt a Support

Pro otázky nebo problémy navštivte soubory kódu a jejich docstrings.

---

## 🎯 Alternativní řešení - Abstraktní turnaje

Projekt obsahuje **tři různé implementace** modulů pro turnaje:

### 1. tournament.py - Originální
- Jedna třída `Tournament` s enum `TournamentType`
- Podmínky `if-elif` v metodě `play()`
- Vhodné pro: Jednoduchost, pochopení problému

### 2. tournament2.py - Vylepšená verze
- Přidáno: místo konání (lokace)
- Přidáno: Koly (přirozené rozdělení)
- Detailnější záznamy zápasů
- Vhodné: Produkční kód s podmínkami

### 3. **tournament_abc.py** ⭐ - Abstraktní dědičnost (NOVÉ)
- `BaseTournament` - abstraktní třída
- `RoundRobinTournament` - konkrétní implementace
- `EliminationTournament` - konkrétní implementace
- **Bez podmínek** - polymorfismus
- **Snadné rozšíření** - přidat nový typ je snadné
- Vhodné: OOP design, tým, budoucí rozšíření

#### Spuštění abstraktní verze

```bash
# Demo program
python tournament_abc_demo.py

# Automatické testy
python tournament_abc_test.py

# Programaticky
python -c "
from game import load_players
from tournament_abc import RoundRobinTournament

players = load_players('players.json')
t = RoundRobinTournament(players, 'Praha')
t.play()
t.print_standings()
"
```

#### Příklad polymorfismu
```python
from tournament_abc import BaseTournament, RoundRobinTournament, EliminationTournament

# Obě třídy jsou kompatibilní přes BaseTournament
tournaments: List[BaseTournament] = [
    RoundRobinTournament(players1, "Praha"),
    EliminationTournament(players2, "Brno")
]

# Polymorfismus - volá se správná implementace
for tournament in tournaments:
    tournament.play()
    tournament.print_standings()
```

**Soubory abstraktní verze:**
- `tournament_abc.py` - Modul (BaseTournament, RoundRobinTournament, EliminationTournament)
- `tournament_abc_demo.py` - Interaktivní demo
- `tournament_abc_test.py` - Automatické testy
- `tournament_abc.md` - Detailní dokumentace
- `ARCHITECTURE.md` - Srovnění všech tří přístupů
- `IMPLEMENTATION_NOTES.md` - Technické poznámky
- `TOURNAMENT_ABC_SUMMARY.md` - Shrnutí

---

**Poslední aktualizace:** 17. února 2026

