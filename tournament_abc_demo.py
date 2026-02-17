"""Demonstrační skript pro abstraktní turnaje.

Ukazuje práci s BaseTournament a jejími podtřídami:
- RoundRobinTournament
- EliminationTournament

Demonstruje polymorfismus a abstraktní dědičnost.
"""

from game import load_players
from tournament_abc import RoundRobinTournament, EliminationTournament


def display_menu():
    """Zobrazí menu pro výběr typu turnaje."""
    print("\n" + "="*70)
    print("ABSTRAKTNÍ TURNAJE - Demonstracni program")
    print("="*70)
    print("\nVyberte typ turnaje:")
    print("1. Kazdy s kazdym (Round-robin)")
    print("2. Eliminacni system (Pavouk)")
    print("3. Ukoncit program")
    print("-"*70)


def get_tournament_location() -> str:
    """Získá místo konání turnaje od uživatele."""
    while True:
        location = input("Zadejte misto konani turnaje: ").strip()
        if location:
            return location
        print("Chyba: Misto musi byt zadano!")


def run_round_robin_tournament():
    """Spustí turnaj formou 'každý s každým'."""
    try:
        players = load_players("players.json")

        if len(players) < 2:
            print(f"Chyba: Pro turnaj je treba alespon 2 hraci. Nacteni: {len(players)}")
            return

        location = get_tournament_location()

        tournament = RoundRobinTournament(
            players=players,
            location=location,
            winning_score=10,
            max_dice_value=6
        )

        print(f"\nVytvoreno: {tournament}")
        tournament.play()
        tournament.print_standings()

        # Uložení výsledků
        filename = f"tournament_abc_rr_{location.lower().replace(' ', '_')}.json"
        tournament.save_tournament_results(filename)

    except FileNotFoundError:
        print("Chyba: Soubor 'players.json' nebyl nalezen!")
    except ValueError as e:
        print(f"Chyba: {e}")
    except Exception as e:
        print(f"Chyba během turnaje: {e}")


def run_elimination_tournament():
    """Spustí eliminační turnaj."""
    try:
        players = load_players("players.json")

        if len(players) < 2:
            print(f"Chyba: Pro turnaj je treba alespon 2 hraci. Nacteni: {len(players)}")
            return

        location = get_tournament_location()

        tournament = EliminationTournament(
            players=players,
            location=location,
            winning_score=10,
            max_dice_value=6
        )

        print(f"\nVytvoreno: {tournament}")
        tournament.play()
        tournament.print_standings()

        # Uložení výsledků
        filename = f"tournament_abc_elim_{location.lower().replace(' ', '_')}.json"
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
            run_round_robin_tournament()
        elif choice == "2":
            run_elimination_tournament()
        elif choice == "3":
            print("\nDekuji za pouziti programu!")
            break
        else:
            print("Chyba: Neznámá volba! Vyberte 1, 2 nebo 3.")


if __name__ == "__main__":
    main()
