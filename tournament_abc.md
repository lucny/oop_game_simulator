# Abstraktní turnaje (tournament_abc.py)

## Přehled

Modul `tournament_abc.py` demonstruje **abstraktní dědičnost** (ABC - Abstract Base Classes) v Pythonu. Místo jedné třídy `Tournament` s podmínkami dle typu se tady používá:

- **BaseTournament** - abstraktní bázová třída
- **RoundRobinTournament** - konkrétní třída pro turnaj "každý s každým"
- **EliminationTournament** - konkrétní třída pro eliminační turnaj

---

## 🏗️ Struktura tříd

```
BaseTournament (ABC - abstraktní třída)
  ├── @abstractmethod play()
  ├── @abstractmethod _print_tournament_header()
  ├── @abstractmethod _get_tournament_type_name()
  ├── @abstractmethod _get_total_rounds()
  └── Společné metody: get_standings(), print_standings(), save_tournament_results()
      │
      ├── RoundRobinTournament
      │   ├── play() - implementace pro round-robin
      │   ├── _print_tournament_header() - záhlaví
      │   ├── _generate_round_robin_schedule() - generování kol
      │   ├── _determine_winner() - určení vítěze
      │   ├── _get_tournament_type_name() → "round_robin"
      │   └── _get_total_rounds() → n-1 kol
      │
      └── EliminationTournament
          ├── play() - implementace pro eliminaci
          ├── _print_tournament_header() - záhlaví
          ├── _get_elimination_round_name() - název kola
          ├── _get_tournament_type_name() → "elimination"
          └── _get_total_rounds() → log₂(n) kol
```

---

## 📋 Detailní popis tříd

### BaseTournament (Abstraktní bázová třída)

Definuje:

**Společné atributy:**
- `players: List[Player]` - seznam hráčů
- `location: str` - místo konání
- `winning_score: int` - body na zápas
- `max_dice_value: int` - maximální hodnota kostky
- `_datetime: datetime` - čas vytvoření
- `matches: List[Match]` - seznam odehraných zápasů
- `winner: Optional[Player]` - vítěz
- `_detailed_results: List[Dict]` - detaily zápasů

**Abstraktní metody (musí být implementovány v podtřídách):**
```python
@abstractmethod
def play(self):
    """Odehraje turnaj dle konkrétního typu."""
    pass

@abstractmethod
def _print_tournament_header(self):
    """Vytiskne záhlaví turnaje."""
    pass

@abstractmethod
def _get_tournament_type_name(self) -> str:
    """Vrací název typu turnaje."""
    pass

@abstractmethod
def _get_total_rounds(self) -> int:
    """Vrací počet kol."""
    pass
```

**Konkrétní implementované metody:**
- `get_standings()` - vrací pořadí hráčů
- `print_standings()` - vyprintuje tabulku
- `save_tournament_results()` - uloží do JSON
- `_print_current_standings()` - průběžné pořadí

---

### RoundRobinTournament

Implementace turnaje "každý s každým".

**Klíčové metody:**
- `play()` - hlavní logika turnaje
- `_generate_round_robin_schedule()` - generuje rozpis kol pomocí round-robin algoritmu
- `_determine_winner()` - určí vítěze podle výher a skóre
- `_print_tournament_header()` - vytiskne "Turnaj: Každý s každým"
- `_get_tournament_type_name()` - vrací "round_robin"
- `_get_total_rounds()` - vrací n-1 (nebo n pokud je lichý počet)

**Příklad použití:**
```python
from game import load_players
from tournament_abc import RoundRobinTournament

players = load_players("players.json")
tournament = RoundRobinTournament(
    players=players,
    location="Praha",
    winning_score=10
)

tournament.play()
tournament.print_standings()
tournament.save_tournament_results("rr_results.json")
```

---

### EliminationTournament

Implementace eliminačního turnaje (pavouk/bracket).

**Klíčové metody:**
- `play()` - hlavní logika eliminačního turnaje
- `_get_elimination_round_name()` - vrací "FINÁLE", "SEMIFINÁLE" atd.
- `_print_tournament_header()` - vytiskne "Turnaj: Eliminační systém"
- `_get_tournament_type_name()` - vrací "elimination"
- `_get_total_rounds()` - vrací log₂(n) zaokrouhleno nahoru

**Příklad použití:**
```python
from tournament_abc import EliminationTournament

tournament = EliminationTournament(
    players=players,
    location="Bratislava",
    winning_score=10
)

tournament.play()
tournament.print_standings()
tournament.save_tournament_results("elim_results.json")
```

---

## 🎯 Výhody abstraktní dědičnosti

### 1. **Čistší separace kódu**
- Cada třída má svou konkrétní logiku
- Nema podmínky typu `if tournament_type == ROUND_ROBIN`
- Kód je lépe organizovaný

### 2. **Polymorfismus**
```python
# Můžeme pracovat s kýmkoliv turnaje stejně:
tournaments = [
    RoundRobinTournament(players, "Praha"),
    EliminationTournament(players, "Brno")
]

for tournament in tournaments:
    tournament.play()  # Volá správnou implementaci
    tournament.print_standings()
```

### 3. **Vynucení implementace**
```python
# Pokud bychom zapomněli implementovat abstraktní metodu:
class MyTournament(BaseTournament):
    pass  # TypeError: Can't instantiate abstract class

# Python automaticky vyvede chybu!
```

### 4. **Jednoduché rozšíření**
```python
# Chceme nový typ turnaje? Jen přidáme třídu:
class SwissSystemTournament(BaseTournament):
    def play(self):
        # Implementace Swiss systému
        pass
    # ... ostatní abstraktní metody
```

### 5. **Type Hints a IDE Support**
```python
def run_tournament(tournament: BaseTournament):
    """IDE ví, že tournament má metodu play() a další."""
    tournament.play()
    standings = tournament.get_standings()
```

---

## 🔄 Srovnání s původní implementací

### tournament.py (s podmínkami)
```python
class Tournament:
    def __init__(self, tournament_type: TournamentType, ...):
        self.tournament_type = tournament_type
    
    def play(self):
        if self.tournament_type == TournamentType.ROUND_ROBIN:
            self._play_round_robin()
        elif self.tournament_type == TournamentType.ELIMINATION:
            self._play_elimination()
```

### tournament_abc.py (s abstraktní dědičností)
```python
class BaseTournament(ABC):
    @abstractmethod
    def play(self):
        pass

class RoundRobinTournament(BaseTournament):
    def play(self):
        # Jen logika round-robin
        ...

class EliminationTournament(BaseTournament):
    def play(self):
        # Jen logika eliminace
        ...
```

**Výhody abstraktní verze:**
- ✅ Jednoduší na čtení a údržbu
- ✅ Méně chyb (žádné podmínky)
- ✅ Snadnější testy (testovat konkrétní třídu)
- ✅ Lepší OOP design

---

## 📝 Praktické příklady

### Příklad 1: Rozlišování turnajů
```python
from tournament_abc import BaseTournament, RoundRobinTournament, EliminationTournament

# Vytvoříme mix turnajů
tournaments = [
    RoundRobinTournament(players1, "Praha"),
    EliminationTournament(players2, "Brno"),
    RoundRobinTournament(players3, "Bratislava")
]

# Všechny jednoduše zpracujeme:
for t in tournaments:
    print(f"Spouštím: {t}")  # Polymorfismus!
    t.play()
    t.print_standings()
    t.save_tournament_results(f"{t._get_tournament_type_name()}.json")
```

### Příklad 2: Ověření typu
```python
from tournament_abc import RoundRobinTournament, EliminationTournament

tournament = RoundRobinTournament(players, "Praha")

if isinstance(tournament, RoundRobinTournament):
    print("Jedná se o turnaj 'každý s každým'")
    print(f"Počet kol: {tournament._get_total_rounds()}")
```

### Příklad 3: Generická funkce
```python
def summarize_tournament(tournament: BaseTournament) -> dict:
    """Společná funkce pro jakýkoliv turnaj."""
    return {
        "type": tournament._get_tournament_type_name(),
        "location": tournament.location,
        "participants": len(tournament.players),
        "rounds": tournament._get_total_rounds(),
        "winner": tournament.winner.nickname if tournament.winner else None
    }

# Funguje pro obě třídy!
rr_info = summarize_tournament(rr_tournament)
elim_info = summarize_tournament(elim_tournament)
```

---

## 🚀 Spuštění

```bash
# Interaktivní demo s menu
python tournament_abc_demo.py

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

---

## 📊 JSON výstup

Struktura je identická s `tournament.py`, liší se jen v poli `type`:

```json
{
  "tournament_info": {
    "type": "round_robin"  // nebo "elimination"
  },
  ...
}
```

---

## 🎓 Vzdělávací hodnota

Modul demonstruje:

1. **ABC (Abstract Base Classes)**
   - `@abstractmethod` dekorátor
   - Vynucování implementace

2. **Dědičnost**
   - Běžná dědičnost z abstraktní třídy
   - Polymorfismus

3. **Design Patterns**
   - Template Method Pattern (abstraktní metody)
   - Strategy Pattern (různé strategie turnajů)

4. **OOP Principy**
   - Abstrakce
   - Zapouzdření
   - Polymorfismus
   - Dědičnost

---

## 🔄 Srovnění s tournament.py a tournament2.py

| Vlastnost | tournament.py | tournament2.py | tournament_abc.py |
|-----------|---|---|---|
| Typy turnajů | 2 (enum) | 2 | 2 (třídy) |
| Koly | Ano | Ano (lepší) | Ano |
| Lokalita | Ano | Ano | Ano |
| Abstraktní třídy | Ne | Ne | **Ano** |
| Podmínky v play() | Ano | Ano | Ne |
| Polymorfismus | Částečný | Částečný | **Plný** |
| Rozšiřitelnost | Střední | Střední | **Vysoká** |

---

## 📝 Poznámky

- `tournament_abc.py` je **alternativa**, ne náhrada `tournament.py`
- Obě verze jsou funkčně ekvivalentní
- Výběr závisí na preferencích programátora
- ABC verze je vhodnější pro větší projekty
- Originální verze je jednodušší pro malé projekty

---

**Poslední aktualizace:** 17. února 2026
