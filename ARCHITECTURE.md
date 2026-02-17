# Architektura turnajů - Srovnění přístupů

Projekt obsahuje **tři implementace** modulů pro turnaje, která demonstruje různé architektonické přístupy:

1. **tournament.py** - Originální přístup s podmínkami (enum)
2. **tournament2.py** - Vylepšená verze s lokalitou a detailními zápisy
3. **tournament_abc.py** - Abstraktní dědičnost (nový přístup)

---

## 📊 Porovnání implementací

| Aspekt | tournament.py | tournament2.py | tournament_abc.py |
|--------|---|---|---|
| **Počet tříd** | 2 (Tournament + TournamentType enum) | 2 (Tournament + TournamentType enum) | 3 (BaseTournament + 2 konkrétní) |
| **Typ rozhodnutí** | if-elif podmínky | if-elif podmínky | Polymorfismus |
| **Lokace** | Ano | Ano | Ano |
| **Koly** | Ano | Ano | Ano |
| **Detailní zápisy** | Ano | Ano (lepší) | Ano |
| **Abstraktní metody** | Ne | Ne | Ano (ABC) |
| **Rozšiřitelnost** | Střední | Střední | Vysoká |
| **Komplexita kódu** | Nízká | Nízká | Střední |
| **OOP Design** | Procedurální | Procedurální | OOP + Design Patterns |

---

## 🔄 Detailní srovnění kódu

### 1. TOURNAMENT.PY - Originální přístup

```python
from enum import Enum

class TournamentType(Enum):
    ROUND_ROBIN = "round_robin"
    ELIMINATION = "elimination"

class Tournament:
    def __init__(self, players, location, tournament_type, ...):
        self.tournament_type = tournament_type
        ...
    
    def play(self):
        if self.tournament_type == TournamentType.ROUND_ROBIN:
            self._play_round_robin()
        elif self.tournament_type == TournamentType.ELIMINATION:
            self._play_elimination()
    
    def _play_round_robin(self):
        # Logika pro round-robin
        ...
    
    def _play_elimination(self):
        # Logika pro eliminaci
        ...
```

**Výhody:**
- ✅ Jednoduchý a přímočarý
- ✅ Málo tříd
- ✅ Snadný na pochopení

**Nevýhody:**
- ❌ Velká třída s mnoha metodami
- ❌ if-elif logika v play()
- ❌ Těžko se rozšiřuje
- ❌ Méně OOP principů

---

### 2. TOURNAMENT2.PY - Vylepšená verze

```python
class Tournament:
    def __init__(self, players, location, tournament_type, ...):
        self.tournament_type = tournament_type
        ...
    
    def play(self):
        if self.tournament_type == TournamentType.ROUND_ROBIN:
            self._play_round_robin()
        elif self.tournament_type == TournamentType.ELIMINATION:
            self._play_elimination()
    
    def _generate_round_robin_schedule(self) -> List[List[Tuple[Player, Player]]]:
        # Lepší algoritmus - koly místo lineárního rozpisu
        ...
```

**Vs tournament.py:**
- ✅ Přidány koly (přirozenější turnaj)
- ✅ Detailnější záznamy zápasů
- ✅ Lépe strukturované JSON

**Zbývající nevýhody:**
- ❌ Stále podmínky v play()
- ❌ Stále jedna velká třída

---

### 3. TOURNAMENT_ABC.PY - Abstraktní dědičnost

```python
from abc import ABC, abstractmethod

class BaseTournament(ABC):
    """Abstraktní bázová třída."""
    
    @abstractmethod
    def play(self):
        pass
    
    @abstractmethod
    def _print_tournament_header(self):
        pass
    
    def get_standings(self):
        # Implementace (společná pro obě podtřídy)
        ...


class RoundRobinTournament(BaseTournament):
    """Konkrétní třída pro round-robin."""
    
    def play(self):
        # Jen logika pro round-robin, bez if-elif
        ...
    
    def _print_tournament_header(self):
        print("TURNAJ: Každý s každým")


class EliminationTournament(BaseTournament):
    """Konkrétní třída pro eliminaci."""
    
    def play(self):
        # Jen logika pro eliminaci, bez if-elif
        ...
    
    def _print_tournament_header(self):
        print("TURNAJ: Eliminační systém")
```

**Výhody vs ostatní:**
- ✅ Čistší separace kódu
- ✅ Žádné if-elif podmínky v play()
- ✅ Polymorfismus
- ✅ Snadné rozšíření o nové typy
- ✅ Abstraktní metody vynucují implementaci
- ✅ Lépe se testuje (každá třída zvlášť)
- ✅ Lepší OOP design

**Nevýhody:**
- ❌ Více tříd (3 místo 1)
- ❌ Mírně složitější na začátku

---

## 🎯 Praktické příklady

### Příklad 1: Vytvoření turnaje

#### tournament.py / tournament2.py
```python
from tournament import Tournament, TournamentType

tournament = Tournament(
    players=players,
    location="Praha",
    tournament_type=TournamentType.ROUND_ROBIN,  # Enum!
    winning_score=10
)
```

#### tournament_abc.py
```python
from tournament_abc import RoundRobinTournament

tournament = RoundRobinTournament(
    players=players,
    location="Praha",
    winning_score=10
)
```

**Rozdíl:**
- V ABC verzi je typ již v názvu třídy
- Není potřeba enum
- IDE lépe podporuje (ví o metodách)

---

### Příklad 2: Spuštění turnaje

Všechny tři verze:
```python
tournament.play()
tournament.print_standings()
tournament.save_tournament_results()
```

**Stejné!** - Rozhraní je identické.

---

### Příklad 3: Polymorfismus

#### tournament.py / tournament2.py
```python
tournaments = [
    Tournament(players1, "Praha", TournamentType.ROUND_ROBIN),
    Tournament(players2, "Brno", TournamentType.ELIMINATION)
]

for t in tournaments:
    t.play()  # Běží správná logika
```

#### tournament_abc.py
```python
from tournament_abc import BaseTournament, RoundRobinTournament, EliminationTournament

tournaments: List[BaseTournament] = [
    RoundRobinTournament(players1, "Praha"),
    EliminationTournament(players2, "Brno")
]

for t in tournaments:
    t.play()  # Běží správná logika
    # IDE ví: t je BaseTournament a má metodu play()
```

**Výhoda ABC:**
- Type hints fungují lépe
- IDE autokomplit funguje lépe
- `isinstance()` funguje přirozeně

---

### Příklad 4: Rozšíření o nový typ

#### tournament.py / tournament2.py
```python
class TournamentType(Enum):
    ROUND_ROBIN = "round_robin"
    ELIMINATION = "elimination"
    SWISS_SYSTEM = "swiss_system"  # Přidat

class Tournament:
    def play(self):
        if self.tournament_type == TournamentType.ROUND_ROBIN:
            self._play_round_robin()
        elif self.tournament_type == TournamentType.ELIMINATION:
            self._play_elimination()
        elif self.tournament_type == TournamentType.SWISS_SYSTEM:  # Přidat
            self._play_swiss_system()  # Přidat
    
    def _play_swiss_system(self):
        # Implementace...
        pass
```

#### tournament_abc.py
```python
class SwissSystemTournament(BaseTournament):
    """Nový typ turnaje - Swiss systém."""
    
    def play(self):
        # Implementace Swiss systému
        pass
    
    def _print_tournament_header(self):
        print("TURNAJ: Swiss systém")
    
    # ... ostatní abstraktní metody
```

**Výhoda ABC:**
- Jen přidáme novou třídu
- Žádné úpravy v existujícím kódu
- Nižší riziko chyb

---

## 🏗️ Architektonické vzory

### tournament.py / tournament2.py

Používá **Procedurální přístup s Enum**:

```
Input (Enum)
    ↓
Tournament.play()
    ↓
if tournament_type == ... (branching)
    ↓
Správná logika
```

**Problém:** Zvětšování počtu `if-elif` s každým novým typem.

---

### tournament_abc.py

Používá **Polymorfismus + Strategy Pattern**:

```
Input (konkrétní třída)
    ↓
BaseTournament.play() (polymorfní)
    ↓
Správná implementace (automaticky)
```

**Výhoda:** Žádné branching, automaticky se volá správná třída.

---

## 📈 Rozhodovací strom

```
Kdy použít tournament.py/tournament2.py?
├─ Malý projekt
├─ Málo turnajových typů
├─ Rychlý prototyp
└─ Nižší komplexita kódu OK

Kdy použít tournament_abc.py?
├─ Větší projekt
├─ Plánujeme více typů turnajů
├─ Testy (mockování)
├─ Předání do týmu
└─ OOP design důležitý
```

---

## 🧪 Testování

### tournament.py / tournament2.py
```python
def test_round_robin_tournament():
    t = Tournament(..., tournament_type=TournamentType.ROUND_ROBIN)
    t.play()
    assert t.winner is not None
    # Ale pokud chceme testovat jen logiku round-robin,
    # musíme zkonstruovat celou třídu s podmínkou
```

### tournament_abc.py
```python
def test_round_robin_tournament():
    t = RoundRobinTournament(...)  # Přesně ví o typu
    t.play()
    assert t.winner is not None
    # Testujeme jen tuto logiku, bez ostatních věcí

def test_polymorphism():
    tournaments: List[BaseTournament] = [
        RoundRobinTournament(...),
        EliminationTournament(...)
    ]
    for t in tournaments:
        t.play()  # Cada se testuje jinak
```

---

## 📊 Metriky kódu

| Metrika | tournament.py | tournament_abc.py |
|---------|---|---|
| Počet řádků v play() | ~150 | 0 (delegováno) |
| Počet if-elif | 2 | 0 |
| Počet tříd | 1 | 3 |
| Cyklomatická komplexita | Vyšší | Nižší |
| Testovatelnost | Nižší | Vyšší |

---

## 🎓 Kdy se učit

**tournament.py** - Pro začátečníky:
- Jednodušší pochopení
- Méně abstrakce

**tournament_abc.py** - Pro pokročilé:
- Abstraktní třídy (ABC)
- Polymorfismus
- Design Patterns
- Profesionální OOP

---

## 📝 Závěr

| Aspekt | tournament.py | tournament_abc.py |
|--------|---|---|
| **Jednoduchost** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Rozšiřitelnost** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **OOP design** | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Testovatelnost** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Vhodnost pro tým** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

**Doporučení:**
- Malý projekt / Učení → **tournament.py**
- Produkční kód / Tým → **tournament_abc.py**

---

**Poslední aktualizace:** 17. února 2026
