# Poznámky k implementaci tournament_abc.py

Detailní technické poznámky k alternativnímu řešení s abstraktní třídou.

---

## 🛠️ Implementační detaily

### 1. Abstraktní bázová třída BaseTournament

#### Import ABC
```python
from abc import ABC, abstractmethod

class BaseTournament(ABC):
    """Abstraktní bázová třída pro všechny turnaje."""
    ...
```

**Vysvětlení:**
- `ABC` - Abstract Base Class
- Neumožňuje přímou instancializaci
- Vynucuje implementaci abstraktních metod v podtřídách

#### Abstraktní metody
```python
@abstractmethod
def play(self):
    """Musí být implementováno."""
    pass
```

**Co se stane, když zapomeneme implementovat?**
```python
class MyTournament(BaseTournament):
    pass  # Chyba!
    # TypeError: Can't instantiate abstract class MyTournament
    # with abstract methods play, _print_tournament_header, ...
```

#### Konkrétní metody
```python
class BaseTournament(ABC):
    def get_standings(self):
        """Toto je normální metoda - je implementováno."""
        standings = []
        for player in self.players:
            score_diff = player.score['plus'] - player.score['minus']
            standings.append((player, player.wins, score_diff))
        standings.sort(key=lambda x: (x[1], x[2]), reverse=True)
        return standings
```

**Podtřídy to dědí automaticky - nemusí reimplementovat.**

---

### 2. Inicializace (\_\_init\_\_)

```python
class BaseTournament(ABC):
    def __init__(self, players: List[Player], location: str,
                 winning_score: int = 10, max_dice_value: int = 6):
        if len(players) < 2:
            raise ValueError("Turnaj vyžaduje alespoň 2 hráče.")
        
        if not location or not location.strip():
            raise ValueError("Místo konání turnaje musí být zadáno.")
        
        self.players = players
        self.location = location.strip()
        ...
```

**Důležité body:**
1. Validace vstupů je v bázové třídě
2. Podtřídy **nevolají** `__init__` znovu
3. `super().__init__()` není potřeba (Python 3.3+)

---

### 3. Polymorfismus v podtřídách

#### RoundRobinTournament
```python
class RoundRobinTournament(BaseTournament):
    def play(self):
        """Implementace pro round-robin."""
        self._print_tournament_header()
        schedule = self._generate_round_robin_schedule()
        # ... zbývající logika
    
    def _print_tournament_header(self):
        """Override abstraktní metody."""
        print("TURNAJ: Každý s každým")
    
    def _generate_round_robin_schedule(self):
        """Metoda specifická jen pro tuto podtřídu."""
        # ... algoritmus round-robin
        pass
```

#### EliminationTournament
```python
class EliminationTournament(BaseTournament):
    def play(self):
        """Implementace pro eliminaci."""
        self._print_tournament_header()
        remaining_players = self.players.copy()
        # ... zbývající logika
    
    def _print_tournament_header(self):
        """Override abstraktní metody."""
        print("TURNAJ: Eliminační systém")
    
    def _get_elimination_round_name(self, num_players: int):
        """Metoda specifická jen pro tuto podtřídu."""
        # ... logika názvů kol
        pass
```

---

### 4. Template Method Pattern

Třída `BaseTournament` využívá pattern "Template Method":

```python
class BaseTournament(ABC):
    # Šablona v save_tournament_results()
    def save_tournament_results(self, filename: str = "tournament_results.json"):
        tournament_data = {
            "tournament_info": {
                "date": self._datetime.strftime("%Y-%m-%d %H:%M:%S"),
                "location": self.location,
                "type": self._get_tournament_type_name(),  # Volá abstraktní metodu
                ...
            },
            ...
            "statistics": {
                "total_rounds": self._get_total_rounds(),  # Volá abstraktní metodu
                ...
            }
        }
        jsonfile_write(filename, tournament_data)
```

**Vysvětlení:**
- Bázová třída definuje **strukturu** (jaké údaje se ukládají)
- Podtřídy definují **konkrétní hodnoty** (jaký je typ turnaje)
- To je Template Method Pattern

---

### 5. Rozdíly v play() metodě

#### RoundRobinTournament.play()
```python
def play(self):
    self._print_tournament_header()
    schedule = self._generate_round_robin_schedule()  # Specifické pro round-robin
    
    for round_num, round_matches in enumerate(schedule, 1):
        # ... hrají se zápasy v kole
        self._detailed_results.append({...})
    
    self._determine_winner()  # Specifické pro round-robin
```

#### EliminationTournament.play()
```python
def play(self):
    self._print_tournament_header()
    remaining_players = self.players.copy()
    round_num = 1
    
    while len(remaining_players) > 1:
        # ... specifická logika eliminace
        next_round_players = [winner1, winner2, ...]
        remaining_players = next_round_players
    
    self.winner = remaining_players[0]  # Vítěz je poslední zbylý
```

**Rozdíl:**
- Round-robin: **Cyklus přes kola** + **určení vítěze podle výher**
- Eliminace: **While smyčka** + **vítěz je poslední hráč**

---

## 🔧 Technické rozhodnutí

### 1. Proč abstraktní metody v BaseTournament?

```python
@abstractmethod
def _get_tournament_type_name(self) -> str:
    pass
```

**Důvod:**
- Každá podtřída má jiný typ ("round_robin", "elimination")
- Bázová třída (save_tournament_results) to potřebuje znát
- Abstraktní metoda vynucuje implementaci v podtřídách

**Alternativa (bez abstraktní metody):**
```python
# Špatně:
def save_tournament_results(self, filename):
    tournament_data = {
        "type": self.tournament_type  # Chyba - atribut neexistuje!
    }
```

---

### 2. Proč _get_total_rounds() jako abstraktní?

```python
@abstractmethod
def _get_total_rounds(self) -> int:
    pass
```

**Logika:**
- Round-robin: počet kol = **n-1** (nebo n+1 pokud lichý počet)
- Eliminace: počet kol = **log₂(n)**

```python
# RoundRobinTournament
def _get_total_rounds(self) -> int:
    n = len(self.players)
    return n - 1 if n % 2 == 0 else n

# EliminationTournament
def _get_total_rounds(self) -> int:
    import math
    n = len(self.players)
    return math.ceil(math.log2(n)) if n > 0 else 0
```

Každá podtřída má svou logiku.

---

### 3. Proč _print_tournament_header() abstraktní?

```python
@abstractmethod
def _print_tournament_header(self):
    pass
```

**Důvod:**
- Záhlaví se liší:
  - Round-robin: "TURNAJ: Každý s každým"
  - Eliminace: "TURNAJ: Eliminační systém"
- Volá se v play() v bázové třídě

**Obsah:**
```python
# RoundRobinTournament
def _print_tournament_header(self):
    print("TURNAJ: Každý s každým")
    print(f"Místo: {self.location}")
    print(f"Počet hráčů: {len(self.players)}")

# EliminationTournament
def _print_tournament_header(self):
    print("TURNAJ: Eliminační systém")
    print(f"Místo: {self.location}")
    print(f"Počet hráčů: {len(self.players)}")
```

---

## 📈 Správa kódu - Kde co je

```
BaseTournament
├─ Inicializace (společná)
├─ __init__ + __str__
├─ Validace
├─ save_tournament_results (šablona)
├─ get_standings (společná logika)
├─ print_standings (společná logika)
│
├─ @abstractmethod play()
├─ @abstractmethod _print_tournament_header()
├─ @abstractmethod _get_tournament_type_name()
└─ @abstractmethod _get_total_rounds()

RoundRobinTournament
├─ Implementace play()
├─ Implementace _print_tournament_header()
├─ Implementace _get_tournament_type_name()
├─ Implementace _get_total_rounds()
│
├─ _generate_round_robin_schedule() (NOVÁ)
└─ _determine_winner() (NOVÁ)

EliminationTournament
├─ Implementace play()
├─ Implementace _print_tournament_header()
├─ Implementace _get_tournament_type_name()
├─ Implementace _get_total_rounds()
│
└─ _get_elimination_round_name() (NOVÁ)
```

---

## 🔍 Debugging a rozšíření

### Jak přidat nový typ turnaje?

```python
class SwissSystemTournament(BaseTournament):
    """Turnaj v Swiss systému."""
    
    def play(self):
        # Implementace Swiss logiky
        print("Spouštím Swiss systém...")
        # ... algoritmus
        self.winner = ...
    
    def _print_tournament_header(self):
        print("TURNAJ: Swiss systém")
    
    def _get_tournament_type_name(self) -> str:
        return "swiss_system"
    
    def _get_total_rounds(self) -> int:
        # Pro Swiss: obvykle ln(n) + 1
        import math
        return math.ceil(math.log(len(self.players))) + 1
```

**A to je vše!** Zbytek (standtings, save) se automaticky dědí.

---

### Ověření, že je vše OK

```python
from tournament_abc import BaseTournament, RoundRobinTournament

# Tyto říádky:
t1 = BaseTournament(...)  # CHYBA - Abstract!
t2 = RoundRobinTournament(...)  # OK
t3 = SwissSystemTournament(...)  # OK
```

---

## 📊 Statistika kódu

```
Soubor              Řádků  Třídy  Metody  Abstraktní
tournament.py       378    2      ~15     0
tournament2.py      ~400   2      ~20     0
tournament_abc.py   ~350   3      ~25     4
```

**Poznámka:**
- Méně řádků díky rozdělení do tříd
- Více metod (templates)
- 4 abstraktní metody

---

## 🧪 Testování podtříd

### Test konkrétní podtřídy
```python
def test_round_robin_specific():
    """Test jen pro round-robin."""
    tournament = RoundRobinTournament(players, "Praha")
    tournament.winning_score = 3
    tournament.play()
    
    # Specifické pro round-robin:
    schedule = tournament._generate_round_robin_schedule()
    assert len(schedule) == len(players) - 1
```

### Test polymorfismu
```python
def test_polymorphism():
    """Test že obě podtřídy mají správné rozhraní."""
    tournaments: List[BaseTournament] = [
        RoundRobinTournament(players1, "Praha"),
        EliminationTournament(players2, "Brno")
    ]
    
    for t in tournaments:
        # Všechny mají tyto metody:
        assert hasattr(t, 'play')
        assert hasattr(t, 'get_standings')
        assert hasattr(t, '_get_tournament_type_name')
```

---

## 🎯 Klíčové poznatky

1. **ABC vynucuje kontrakt**: Každá podtřída MUSÍ implementovat všechny abstraktní metody

2. **Polymorfismus funguje automaticky**: Volání `t.play()` na libovolném `BaseTournament` vede na správnou implementaci

3. **Kód je čistší**: Žádné `if tournament_type == ...` v play()

4. **Snadnější rozšíření**: Nový typ = nová třída, bez změn v existujícím kódu

5. **Lepší testy**: Testujeme konkrétní třídu, ne podmínky v if-elif

---

## 📚 Zdroje

- [PEP 3119 - Abstract Base Classes](https://www.python.org/dev/peps/pep-3119/)
- [Python docs - abc module](https://docs.python.org/3/library/abc.html)
- [Design Patterns - Template Method](https://refactoring.guru/design-patterns/template-method)

---

**Poslední aktualizace:** 17. února 2026
