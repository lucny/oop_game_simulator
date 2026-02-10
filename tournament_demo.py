"""Ukázkový skript pro demonstraci vylepšených turnajů.

Načte hráče a odehraje turnaj s pokročilými funkcemi:
- Místo konání
- Kola v round-robin formátu
- Detailní záznamy zápasů
"""

from game import load_players
from tournament2 import Tournament, TournamentType


def main():
    """Demonstrace vylepšených turnajů."""
    print("="*70)
    print("POKROČILÝ SIMULÁTOR TURNAJŮ")
    print("="*70)
    
    try:
        players = load_players("players.json")
    except FileNotFoundError:
        print("Chyba: Soubor 'players.json' nebyl nalezen.")
        return
    except Exception as e:
        print(f"Chyba při načítání hráčů: {e}")
        return

    if len(players) < 2:
        print("Nedostatek hráčů pro turnaj. Potřebujeme alespoň 2 hráče.")
        return

    print(f"\nNačteno {len(players)} hráčů:")
    for player in players:
        print(f"  - {player.nickname} ({player.state})")

    # Zadání místa konání
    print("\n" + "="*70)
    location = input("Zadejte místo konání turnaje: ").strip()
    if not location:
        location = "Praha"
        print(f"Použito výchozí místo: {location}")

    # Menu pro výběr typu turnaje
    print("\n" + "="*70)
    print("Vyberte typ turnaje:")
    print("1. Každý s každým (Round-robin) - organizováno do kol")
    print("2. Eliminační systém (Pavouk)")
    
    choice = input("\nVaše volba (1/2): ").strip()
    
    if choice == "1":
        tournament_type = TournamentType.ROUND_ROBIN
    elif choice == "2":
        tournament_type = TournamentType.ELIMINATION
    else:
        print("Neplatná volba, použiji Round-robin")
        tournament_type = TournamentType.ROUND_ROBIN

    try:
        # Vytvoření a odehrání turnaje
        tournament = Tournament(
            players=players,
            location=location,
            tournament_type=tournament_type,
            winning_score=10,
            max_dice_value=6
        )
        
        print(f"\n{tournament}")
        tournament.play()
        tournament.print_standings()
        
        # Uložení výsledků
        filename = f"tournament_{location.lower().replace(' ', '_')}_{tournament_type.value}.json"
        tournament.save_tournament_results(filename)
        
        print(f"\n{'='*70}")
        print("Turnaj byl úspěšně dokončen!")
        print(f"{'='*70}\n")
        
    except ValueError as e:
        print(f"Chyba při vytváření turnaje: {e}")
    except Exception as e:
        print(f"Neočekávaná chyba: {e}")


if __name__ == "__main__":
    main()
