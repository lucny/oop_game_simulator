from game import load_players, Match


def main():
    # Načtení hráčů ze souboru
    players = load_players("players.json")

    if len(players) < 2:
        print("Nedostatek hráčů pro zápas.")
        return

    # Výběr prvních dvou hráčů pro simulaci zápasu
    player1 = players[0]
    player2 = players[1]

    print(f"Zápas mezi {player1.nickname} a {player2.nickname} právě začíná!")

    # Vytvoření zápasu a jeho odehrání
    match = Match(player1, player2, winning_score=10, max_dice_value=6)
    match.play()

    # Výpis výsledků
    print(f"Výsledek: {match}")
    print("Vývoj skóre během zápasu:", match.get_history())

    # Uložení výsledků zápasu
    match.save_match_results("results.json")
    print("Výsledek zápasu uložen.")


if __name__ == "__main__":
    main()
