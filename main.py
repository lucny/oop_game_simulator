"""Demonstrační program pro simulaci turnajů.

Hlavní program pro spuštění turnajů různých typů:
- Round-robin (každý s každým)
- Elimination (vyřazovací systém/pavouk)

Využívá TournamentFactory pro vytváření turnajů a demonstruje
polymorfismus a abstraktní dědičnost.
"""

from game import load_players
from tournament import TournamentFactory


def display_menu():
    """Zobrazí menu pro výběr typu turnaje."""
    print("\n" + "="*70)
    print("SIMULÁTOR TURNAJŮ - Demonstrační program")
    print("="*70)
    print("\nVyberte typ turnaje:")
    print("1. Každý s každým (Round-robin)")
    print("2. Eliminační systém (Pavouk)")
    print("3. Ukončit program")
    print("-"*70)


def get_tournament_location() -> str:
    """Získá místo konání turnaje od uživatele."""
    while True:
        location = input("Zadejte místo konání turnaje: ").strip()
        if location:
            return location
        print("Chyba: Místo musí být zadáno!")


def run_tournament(tournament_type: str):
    """Spustí turnaj podle zadaného typu pomocí TournamentFactory.
    
    Args:
        tournament_type (str): Typ turnaje ("round_robin" nebo "elimination").
    """
    try:
        players = load_players("players.json")

        if len(players) < 2:
            print(f"Chyba: Pro turnaj je třeba alespoň 2 hráči. Načteno: {len(players)}")
            return

        location = get_tournament_location()

        # Použití TournamentFactory
        tournament = TournamentFactory.create(
            tournament_type=tournament_type,
            players=players,
            location=location,
            winning_score=10,
            max_dice_value=6
        )

        print(f"\nVytvořeno: {tournament}")
        tournament.play()
        tournament.print_standings()

        # Uložení výsledků
        type_abbr = "rr" if tournament_type == "round_robin" else "elim"
        filename = f"tournament_{type_abbr}_{location.lower().replace(' ', '_')}.json"
        tournament.save_tournament_results(filename)

    except FileNotFoundError:
        print("Chyba: Soubor 'players.json' nebyl nalezen!")
    except ValueError as e:
        print(f"Chyba: {e}")
    except Exception as e:
        print(f"Chyba během turnaje: {e}")


def main():
    """Hlavní smyčka programu."""
    while True:
        display_menu()
        choice = input("Vaše volba (1-3): ").strip()

        if choice == "1":
            run_tournament("round_robin")
        elif choice == "2":
            run_tournament("elimination")
        elif choice == "3":
            print("\nDěkuji za použití programu!")
            break
        else:
            print("Chyba: Neznámá volba! Vyberte 1, 2 nebo 3.")


if __name__ == "__main__":
    main()
