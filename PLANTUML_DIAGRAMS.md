# PlantUML Diagramy - Abstraktní Architektura

Podrobný popis všech diagramů v souboru `plantuml2.txt`.

---

## 📊 Obsah plantuml2.txt

Soubor obsahuje **8 diagramů** demonstrujících strukturu a chování nového abstraktního řešení:

1. **Class_Diagram_ABC_Architecture** - Diagramy tříd
2. **Inheritance_Hierarchy** - Hierarchie dědičnosti
3. **Polymorphism_Example** - Příklad polymorfismu
4. **Template_Method_Pattern** - Vzor šablony metody
5. **Abstract_Method_Enforcement** - Vynucení abstraktních metod
6. **Sequence_RoundRobin_Play** - Sekvence Round-robin
7. **Sequence_Elimination_Play** - Sekvence Eliminace
8. **Comparison_Architecture** - Srovnění architektur
9. **Usage_Example** - Příklad použití

---

## 🎯 Diagram 1: Class_Diagram_ABC_Architecture

### Obsah
Komplexní diagram ukazující všechny třídy a jejich vztahy.

### Package `game`
```
Gender (enum)
Dice (statická třída)
Person (základní třída)
  └── Player (dědí z Person)
Match (zápas, používá Player a Dice)
```

### Package `tournament_abc`
```
BaseTournament (ABC - abstraktní)
  ├── play() {abstract}
  ├── _print_tournament_header() {abstract}
  ├── _get_tournament_type_name() {abstract}
  ├── _get_total_rounds() {abstract}
  ├── get_standings() {konkrétní}
  ├── print_standings() {konkrétní}
  └── save_tournament_results() {konkrétní}

RoundRobinTournament (dědí z BaseTournament)
  ├── play() - implementace
  ├── _print_tournament_header() - "Každý s každým"
  ├── _generate_round_robin_schedule() - specifické
  └── _determine_winner() - specifické

EliminationTournament (dědí z BaseTournament)
  ├── play() - implementace
  ├── _print_tournament_header() - "Eliminační systém"
  └── _get_elimination_round_name() - specifické
```

### Vztahy
- **`Player --|> Person`** - RoundRobinTournament dědí z BaseTournament
- **`EliminationTournament --|> BaseTournament`** - EliminationTournament dědí z BaseTournament
- **`BaseTournament o-- Match`** - Turnaj obsahuje zápasy
- **`BaseTournament o-- Player`** - Turnaj obsahuje hráče

---

## 📚 Diagram 2: Inheritance_Hierarchy

### Obsah
Zjednodušený diagram hierarchie dědičnosti.

```
         BaseTournament
              △
              │
    ┌─────────┴──────────┐
    │                    │
RoundRobinTournament  EliminationTournament
```

### Vysvětlení

**BaseTournament (ABC)**
- Abstraktní třída
- Vynucuje implementaci abstraktních metod
- Definuje společné atributy

**RoundRobinTournament**
- Konkrétní třída
- Implementuje `play()` pro round-robin
- Má `_generate_round_robin_schedule()`
- Turnaj "Každý s každým" v N-1 kolech

**EliminationTournament**
- Konkrétní třída
- Implementuje `play()` pro eliminaci
- Má while smyčku místo for
- Turnaj "Pavouk" s vyřazením

---

## 🔄 Diagram 3: Polymorphism_Example

### Obsah
Sekvence demonstrujující polymorfismus.

### Kód
```python
tournaments = [
    RoundRobinTournament(players, "Praha"),
    EliminationTournament(players, "Brno")
]

for tournament in tournaments:
    tournament.play()  # Volá správnou implementaci!
    tournament.print_standings()
```

### Vysvětlení

**Polymorfismus:**
- `tournament.play()` - Každá třída má svou implementaci
- **RoundRobinTournament.play()** - Generuje kola, hrají se zápasy
- **EliminationTournament.play()** - While smyčka, postupují vítězové

**Bez if-elif!**
- Původně: `if tournament_type == ROUND_ROBIN: ...`
- Teď: Automaticky se volá správná třída

---

## 📋 Diagram 4: Template_Method_Pattern

### Obsah
Demonstruje Template Method Pattern v `save_tournament_results()`.

### Princip

**BaseTournament.save_tournament_results()**
```
Definuje strukturu JSON:
├─ tournament_info
├─ players
├─ winner
├─ matches
├─ final_standings
└─ statistics

Volá abstraktní metody:
├─ _get_tournament_type_name()  (variabilní část)
└─ _get_total_rounds()          (variabilní část)
```

**RoundRobinTournament._get_tournament_type_name()**
```
return "round_robin"
```

**EliminationTournament._get_tournament_type_name()**
```
return "elimination"
```

### Výhoda

- Bázová třída definuje **ŠABLONU** (strukturu)
- Podtřídy vyplňují **KONKRÉTNÍ HODNOTY**
- Bez duplikace kódu

---

## 🛡️ Diagram 5: Abstract_Method_Enforcement

### Obsah
Ukazuje, co se stane, když zapomeneme implementovat abstraktní metodu.

### Tři scénáře

**1. IncompleteImplementation (CHYBA)**
```python
class IncompleteImplementation(BaseTournament):
    def play(self):
        # ✗ Chybí: _print_tournament_header()
        pass

# Chyba při instancializaci:
# TypeError: Can't instantiate abstract class IncompleteImplementation
# with abstract methods _print_tournament_header, ...
```

**2. RoundRobinTournament (OK)**
```python
class RoundRobinTournament(BaseTournament):
    def play(self): ...
    def _print_tournament_header(self): ...
    def _get_tournament_type_name(self): ...
    def _get_total_rounds(self): ...
    # ✓ Všechny abstraktní metody implementovány
```

**3. EliminationTournament (OK)**
```python
class EliminationTournament(BaseTournament):
    def play(self): ...
    def _print_tournament_header(self): ...
    def _get_tournament_type_name(self): ...
    def _get_total_rounds(self): ...
    # ✓ Všechny abstraktní metody implementovány
```

### Výhoda

Python automaticky **vyvádí chybu** pokud chybí implementace!

---

## ⏱️ Diagram 6: Sequence_RoundRobin_Play

### Obsah
Sekvence kroků při spuštění RoundRobinTournament.

### Kroky

```
1. Client -> RoundRobinTournament.play()

2. _print_tournament_header()
   └─ Vytiskne: "TURNAJ: Každý s každým"

3. _generate_round_robin_schedule()
   ├─ Vypočítá počet hráčů: n
   ├─ Pokud lichý: přidá BYE
   ├─ Generuje n-1 kol
   ├─ V každém kole: párování a rotace
   └─ Vrací: List[List[Tuple[Player, Player]]]

4. for round_num, round_matches in schedule:
   for player1, player2 in round_matches:
   ├─ Vytvoří Match(player1, player2)
   ├─ match.play() - Zápas se hraje
   ├─ Uloží detaily (skóre, historii, vítěze)
   └─ _detailed_results.append({...})

5. _print_current_standings()
   └─ Vytiskne mezivýsledky po každém kole

6. _determine_winner()
   ├─ Najde hráče s max výhrami
   ├─ Případně tiebreak (lepší skóre)
   └─ Nastaví self.winner
```

### Výstup
- Turnaj odehrán
- winner nastavený
- _detailed_results naplněný

---

## ⏱️ Diagram 7: Sequence_Elimination_Play

### Obsah
Sekvence kroků při spuštění EliminationTournament.

### Kroky

```
1. Client -> EliminationTournament.play()

2. _print_tournament_header()
   └─ Vytiskne: "TURNAJ: Eliminační systém"

3. remaining_players = players.copy()
   round_num = 1

4. while len(remaining_players) > 1:
   ├─ round_name = _get_elimination_round_name()
   │  (FINÁLE, SEMIFINÁLE, ČTVRTFINÁLE, ...)
   │
   ├─ Alt: Lichý počet hráčů?
   │  ├─ bye_player = remaining_players[0]
   │  ├─ Vytiskne: "Postupuje automaticky"
   │  └─ next_round_players = [bye_player]
   │
   ├─ for i in range(0, len(remaining), 2):
   │  ├─ player1, player2 = remaining[i:i+2]
   │  ├─ Match(player1, player2).play()
   │  ├─ winner se přidá do next_round_players
   │  ├─ Uloží detaily (skóre, vítěze, vyřazeného)
   │  └─ _detailed_results.append({...})
   │
   ├─ remaining_players = next_round_players
   └─ round_num += 1

5. self.winner = remaining_players[0]
   └─ Poslední zbylý hráč je vítěz
```

### Výstup
- Turnaj odehrán
- winner nastavený (poslední zbylý)
- _detailed_results naplněný

---

## 🔄 Diagram 8: Comparison_Architecture

### Obsah
Srovnění původního přístupu (tournament.py) vs nového (tournament_abc.py).

### tournament.py (Procedurální)
```
1 třída Tournament
├─ if tournament_type == TournamentType.ROUND_ROBIN
├─ elif tournament_type == TournamentType.ELIMINATION
└─ Problém: Spaghetti kód, těžko se rozšiřuje
```

### tournament_abc.py (OOP)
```
BaseTournament (ABC)
├─ RoundRobinTournament
│  └─ Specifické pro round-robin
└─ EliminationTournament
   └─ Specifické pro eliminaci

Výhody:
├─ Čistý kód
├─ Bez if-elif
├─ Snadné rozšíření
└─ Polymorfismus
```

---

## 📱 Diagram 9: Usage_Example

### Obsah
Reálný příklad použití nového řešení.

### Kód
```python
# Vytvoření turnajů
t1 = RoundRobinTournament(players, "Praha")
t2 = EliminationTournament(players, "Brno")

# Spuštění
t1.play()     # Běží RoundRobinTournament.play()
t2.play()     # Běží EliminationTournament.play()

# Výsledky
t1.print_standings()
t2.save_tournament_results()
```

### Polymorfismus
```
Stejná rozhraní:
├─ play()
├─ print_standings()
├─ save_tournament_results()
└─ get_standings()

Různé implementace:
├─ t1.play() → round-robin logika
└─ t2.play() → eliminace logika
```

---

## 🎨 Viz a barvy

PlantUML soubor používá:

| Diagram | Barva | Téma |
|---------|-------|------|
| Class | Světle modrá | Abstraktní architektura |
| Inheritance | Zlatá | Hierarchie |
| Polymorphism | Šedá | Sekvenční |
| Template Method | Zelená | Pattern |
| Abstract Enforcement | Oranžová | Error handling |
| Sequences | Modrá | Interakce |
| Comparison | Purpurová | Srovnění |
| Usage | Modrá | Praktika |

---

## 🚀 Jak zobrazit diagramy

### Online editor
1. Jít na https://www.plantuml.com/plantuml/uml/
2. Zkopírovat kód z plantuml2.txt
3. Vložit do editoru
4. Vygeneruje PNG/SVG

### VS Code rozšíření
1. Instalovat "PlantUML" rozšíření
2. Otevřít plantuml2.txt
3. Alt+D pro zobrazení

### Lokálně
```bash
# Pokud máte PlantUML nainstalován
plantuml plantuml2.txt
```

---

## 📊 Statistika

- **Řádky kódu:** 536
- **Diagramů:** 9
- **Tříd:** 3 (BaseTournament, RoundRobinTournament, EliminationTournament)
- **Balíčků:** 2 (game, tournament_abc)
- **Vzorů:** Template Method, Strategy, Polymorphism

---

## 🎓 Vzdělávací hodnota

Diagramy demonstruje:

1. **Abstraktní dědičnost** - ABC třídy
2. **Polymorfismus** - Různé implementace
3. **Design Patterns** - Template Method
4. **Sekvence** - Tok provádění
5. **Srovnění** - Staré vs nové řešení
6. **Praktické aplikace** - Reálné použití

---

## 📝 Poznámky

- Diagramy jsou komplimentární k `tournament_abc.py`
- Každý diagram se fokusuje na jednu aspekt
- Kombinací můžete pochopit celou architekturu
- Všechny diagramy jsou v jednom souboru `plantuml2.txt`

---

**Poslední aktualizace:** 17. února 2026
