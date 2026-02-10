"""Hlavní modul pro simulaci zápasu mezi dvěma hráči.

Načítá hráče ze souboru, vytvoří zápas a uloží výsledky.
"""

from game import load_players, Match


def main():
    """Orchestruje simulaci zápasu mezi dvěma hráči a ukládá výsledky."""
    try:
        players = load_players("players.json")
    except FileNotFoundError:
        print("Chyba: Soubor 'players.json' nebyl nalezen.")
        return
    except Exception as e:
        print(f"Chyba při načítání hráčů: {e}")
        return

    if len(players) < 2:
        print("Nedostatek hráčů pro zápas. Potřebujeme alespoň 2 hráče.")
        return

    player1 = players[0]
    player2 = players[1]

    print(f"Zápas mezi {player1.nickname} a {player2.nickname} právě začíná!")

    try:
        match = Match(player1, player2, winning_score=10, max_dice_value=6)
        match.play()

        print(f"Výsledek: {match}")
        print("Vývoj skóre během zápasu:", match.get_history())

        match.save_match_results("results.json")
        print("Výsledek zápasu uložen.")
    except TypeError as e:
        print(f"Chyba při vytváření nebo hrání zápasu: {e}")
    except IOError as e:
        print(f"Chyba při ukládání výsledků: {e}")
    except Exception as e:
        print(f"Neočekávaná chyba: {e}")


if __name__ == "__main__":
    main()
