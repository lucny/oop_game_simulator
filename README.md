# OOP Game Simulator - Simulátor her a turnajů

## 📋 Obsah

1. [Přehled projektu](#přehled-projektu)
2. [Architektura a struktura tříd](#architektura-a-struktura-tříd)
3. [Instalace a spuštění](#instalace-a-spuštění)
4. [Moduly a jejich popis](#moduly-a-jejich-popis)
5. [Datové struktury](#datové-struktury)
6. [Algoritmy](#algoritmy)
7. [Příklady použití](#příklady-použití)
8. [Datové soubory](#datové-soubory)
9. [Pokročilé funkce](#pokročilé-funkce)
10. [Optimalizace a standardy](#optimalizace-a-standardy)

---

## 🎯 Přehled projektu

**OOP Game Simulator** je Python aplikace pro simulaci her a turnajů mezi více hráči. Projekt demonstruje objektově orientované programování s využitím dědičnosti, polimorfismu a různých enumerací.

### Hlavní funkce:
- ✅ Simulace jednotlivých zápasů mezi dvěma hráči
- ✅ Turnaje formou **Round-robin** (každý s každým)
- ✅ Turnaje formou **Eliminace** (vyřazovací systém/pavouk)
- ✅ Detailní záznamy zápasů a turnajů do JSON
- ✅ Načítání a ukládání dat ze/do souborů (JSON, CSV, textové)
- ✅ Komprehenzivní ošetření výjimek
- ✅ Dodržování PEP 8 standardů

---

## 🏗️ Architektura a struktura tříd

### Hierarchie tříd

```
Person (osoba s přezdívkou, pohlavím, datem narození)
  └── Player (hráč s stavem, zápasy, výhry, skóre)

Dice (statická třída pro hod kostkou)

Match (zápas mezi dvěma hráči)
  └── interactions with: Player, Dice

Tournament (turnaj s hráči a zápasy)
  └── contains: List[Player], List[Match]
  └── uses: TournamentType (Enum)

Gender (Enum: male, female)
TournamentType (Enum: ROUND_ROBIN, ELIMINATION)
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

#### **Tournament (Turnaj)**
Organizuje turnaj mezi více hráči.

**Atributy:**
- `players: List[Player]` - seznam hráčů
- `location: str` - místo konání turnaje
- `tournament_type: TournamentType` - typ turnaje
- `winning_score: int` - body na zápas
- `max_dice_value: int` - maximální hodnota kostky
- `matches: List[Match]` - seznam odehraných zápasů
- `winner: Optional[Player]` - vítěz turnaje
- `_detailed_results: List[Dict]` - detailní záznamy

**Klíčové metody:**
- `play() -> None` - odehraje turnaj dle typu
- `get_standings() -> List[Tuple]` - vrací pořadí hráčů
- `print_standings() -> None` - vyprintuje tabulku
- `save_tournament_results(filename) -> None` - uloží detailní výsledky

**Privátní metody:**
- `_play_round_robin() -> None` - turnaj "každý s každým"
- `_play_elimination() -> None` - turnaj "pavouk"
- `_generate_round_robin_schedule() -> List` - generuje rozpis kol
- `_determine_round_robin_winner() -> None` - určí vítěze

---

## 🚀 Instalace a spuštění

### Požadavky
- Python 3.7+
- Standardní knihovny (json, csv, datetime, enum, random)

### Instalace
```bash
# Klonování nebo stažení projektu
cd d:\ukoly\python\oop_game_simulator

# Žádné další závislosti se neinstalují (pouze stdlib)
```

### Spuštění

#### Jednoduchý zápas
```bash
python main.py
```
Načte hráče z `players.json`, odehraje zápas mezi prvními dvěma a uloží výsledky.

#### Turnaj Round-robin
```bash
python tournament_demo.py
# Vybrat volbu: 1
```

#### Turnaj Eliminace
```bash
python tournament_demo.py
# Vybrat volbu: 2
```

#### Pokročilý turnaj s lokalitou
```bash
python tournament2_demo.py
# Zadej místo: Praha
# Vybrat typ turnaje
```

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
Rozšířené moduly pro turnaje.

**tournament.py:**
- Základní implementace turnajů
- Round-robin: generování a odehrávání zápasů
- Eliminace: vyřazovací systém

#### Algoritmus Round-robin:
Generuje rozpis kol tak, aby každý hráč hrál v každém kole max. jednou:
- Pro n hráčů se vytvoří n-1 kol
- Při lichém počtu jeden hráč má v daném kole "volno" (BYE)
- Algoritmus rotace: první hráč zůstává, ostatní rotují

#### Algoritmus Eliminace:
Vyřazovací systém s podporou lichého počtu hráčů:
- Páry hrají zápasy, vítěz postupuje
- Při lichém počtu: první hráč automaticky postupuje
- Pokračuje dokud zbývá 1 hráč (vítěz)

### **main.py**
Jednoduchý vstupní bod pro spuštění zápasu.

Plní funkci:
1. Načte hráče z `players.json`
2. Ověří, že jsou alespoň 2 hráči
3. Vytvoří a odehraje `Match` mezi prvními dvěma
4. Vyprintuje výsledek a historii
5. Uloží výsledky do `results.json`

### **tournament_demo.py**
Interaktivní skripty pro turnaje s výběrem typu.

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

### **results.json** (Výstup - zápas)
```json
[
  {
    "date": "2026-02-09 15:30:45",
    "house_player": "Jan",
    "guest_player": "Marie",
    "score": [10, 7]
  }
]
```

### **tournament_results.json** (Výstup - turnaj)
```json
{
  "tournament_info": {
    "date": "2026-02-09 15:45:00",
    "location": "Praha",
    "type": "round_robin",
    "winning_score": 10,
    "max_dice_value": 6
  },
  "players": [
    {"nickname": "Jan", "state": "CZ", "gender": "man"},
    {"nickname": "Marie", "state": "SK", "gender": "woman"}
  ],
  "winner": {
    "nickname": "Jan",
    "state": "CZ",
    "total_wins": 3,
    "total_games": 3,
    "win_rate": 100.0
  },
  "matches": [
    {
      "round": 1,
      "match_type": "round_robin",
      "player1": {"nickname": "Jan", "state": "CZ"},
      "player2": {"nickname": "Marie", "state": "SK"},
      "final_score": {"player1": 10, "player2": 7},
      "winner": "Jan",
      "score_history": [[1,0], [2,0], [2,1]],
      "match_duration": 15
    }
  ],
  "final_standings": [
    {
      "position": 1,
      "player": "Jan",
      "state": "CZ",
      "wins": 3,
      "games": 3,
      "score_plus": 30,
      "score_minus": 18,
      "score_difference": 12,
      "win_rate": 100.0
    }
  ],
  "statistics": {
    "total_matches": 3,
    "total_rounds": 3,
    "average_match_duration": 15.33
  }
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
- Přírodní organizace turnaje

### Elimination Algoritmus (Vyřazovací systém)

```
1. Vstup: seznam hráčů (remaining_players)
2. Dokud je více než 1 hráč:
   a. Pokud je počet hráčů lichý:
      - První hráč automaticky postupuje
   b. Zbylé hráče spáruj
   c. Pro každou páru:
      - Odehraj zápas
      - Vítěz postupuje do dalšího kola
      - Poražený je vyřazen
   d. Aktualizuj seznam hráčů na vítěze
3. Výstup: poslední zbylý hráč = vítěz
```

**Charakteristika:**
- Počet kol: log₂(n) (zaokrouhleno nahoru)
- Méně zápasů: n-1 (vs. n*(n-1)/2 u round-robin)
- Tradiční tenis, fotbal playoff systém

---

## 💡 Příklady použití

### Příklad 1: Načtení a jednoduché otestování
```python
from game import load_players, Match

# Načti hráče
players = load_players("players.json")

# Vytvoř zápas
match = Match(players[0], players[1], winning_score=10)

# Odehraj
match.play()

# Výsledek
print(f"Skóre: {match.score()}")
print(f"Vítěz: {match.h_player if match.score()[0] > match.score()[1] else match.g_player}")
```

### Příklad 2: Round-robin turnaj
```python
from game import load_players
from tournament2 import Tournament, TournamentType

players = load_players("players.json")
tournament = Tournament(
    players=players,
    location="Praha",
    tournament_type=TournamentType.ROUND_ROBIN,
    winning_score=10,
    max_dice_value=6
)

tournament.play()
tournament.print_standings()
tournament.save_tournament_results("tournament_rr.json")
```

### Příklad 3: Eliminační turnaj
```python
from tournament2 import Tournament, TournamentType

tournament = Tournament(
    players=players,
    location="Bratislava",
    tournament_type=TournamentType.ELIMINATION,
    winning_score=10
)

tournament.play()
tournament.print_standings()
tournament.save_tournament_results("tournament_elim.json")
```

### Příklad 4: Vlastní hráči
```python
from game import Player, Gender

player1 = Player("Alice", Gender.female, "CZ")
player2 = Player("Bob", Gender.male, "SK")

# Manuálně lze přidat do turnaje
players = [player1, player2]
tournament = Tournament(players, "Brno")
```

---

## 📊 Datové soubory

### Konfigurace
Projektu **nevyžaduje** konfigurační soubory (konf. jsou hardcodnuty v kódu).

### Vstupy
- **players.json** - seznam hráčů (povinný pro `load_players()`)

### Výstupy (auto-generované)
- **results.json** - výsledky jednotlivých zápasů
- **tournament_results.json** - detailní výsledky turnaje
- **tournament_*.json** - turnaje s konkrétní lokalitou a typem

---

## 🔧 Pokročilé funkce

### 1. Vlastní validace dat
- Pohlaví: enum `Gender` (only 'man' nebo 'woman')
- Počet výher: nesmí být záporný
- Hráči v zápase: instance `Player`
- CSV data: seznam neprázdných slovníků

### 2. Ošetření výjimek
Všechny moduly vyvolávají specifické výjimky:
- `FileNotFoundError` - soubor neexistuje
- `json.JSONDecodeError` - nevalidní JSON
- `KeyError` - chybí klíč v datech
- `ValueError` - nevalidní vstup
- `TypeError` - špatný typ
- `IOError` - chyba I/O operace

Volající kód musí tyto výjimky zachytit:
```python
try:
    players = load_players("players.json")
except FileNotFoundError:
    print("Soubor nenalezen!")
except ValueError as e:
    print(f"Chyba v datech: {e}")
```

### 3. Práce s historií skóre
```python
match = Match(player1, player2)
match.play()

# Historii lze získat
history = match.get_history()
# Výstup: [(1,0), (2,0), (2,1), (2,2), (3,2), ...]

# V JSON je zaznamenána úplná historie
```

### 4. Statistiky turnaje
```python
tournament = Tournament(players, "Praha")
tournament.play()

standings = tournament.get_standings()
# vrací: [(Player, wins, score_diff), ...]

# JSON obsahuje:
# - Průměrné trvání zápasu
# - Počet kol/zápasů
# - Konečné pořadí se všemi metrikami
```

---

## ✅ Optimalizace a standardy

### PEP 8 Compliance
- ✅ Jména tříd: CamelCase (`Person`, `Match`, `Tournament`)
- ✅ Jména funkcí/metod: snake_case (`load_players`, `save_match_results`)
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

tournament: Tournament = Tournament(
    players=players,
    location="Praha",
    tournament_type=TournamentType.ROUND_ROBIN
)
```

### Error Handling
- ✅ Vyvolávání specifických výjimek místo `print()`
- ✅ Kaskádované try-except bloky pro detail
- ✅ Jasné chybové zprávy s kontextem
- ✅ Validace vstupů na počátku funkcí

### Code Organization
- ✅ Moduly rozděleny dle funkce (files, game, tournament)
- ✅ Soubor `plantuml.txt` pro vizualizaci architektury
- ✅ `README.md` pro dokumentaci
- ✅ Jednoduchý `main.py` jako entry point

---

## 🎓 Vzdělávací prvky

Projekt demonstruje:

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

