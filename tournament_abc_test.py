"""Test skript pro abstraktní turnaje - programatické spuštění.

Demonstruje práci s TournamentFactory a polymorfismem.
"""

from game import load_players
from tournament_abc import TournamentFactory, RoundRobinTournament, EliminationTournament


def test_round_robin():
    """Testuje round-robin turnaj."""
    print("\n" + "="*70)
    print("TEST 1: Round-robin turnaj")
    print("="*70)
    
    try:
        players = load_players("players.json")
        
        if len(players) < 2:
            print(f"Nedostatek hracu: {len(players)}")
            return False
        
        tournament = RoundRobinTournament(
            players=players,
            location="Praha",
            winning_score=10,
            max_dice_value=6
        )
        
        print(f"Vytvoreno: {tournament}")
        print(f"Typ turnaje: {tournament._get_tournament_type_name()}")
        print(f"Ocekavany pocet kol: {tournament._get_total_rounds()}")
        
        # Krátký turnaj - snížíme počet bodů
        tournament.winning_score = 3
        
        tournament.play()
        tournament.print_standings()
        
        print(f"\nVítěz: {tournament.winner.nickname if tournament.winner else 'None'}")
        print(f"Počet zápasů: {len(tournament.matches)}")
        print(f"Počet detailů: {len(tournament._detailed_results)}")
        
        print("\nOK - Round-robin test byl uspesny!")
        return True
        
    except Exception as e:
        print(f"\nCHYBA - Chyba při testu: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_elimination():
    """Testuje eliminační turnaj."""
    print("\n" + "="*70)
    print("TEST 2: Eliminacni turnaj")
    print("="*70)
    
    try:
        players = load_players("players.json")
        
        if len(players) < 2:
            print(f"Nedostatek hracu: {len(players)}")
            return False
        
        tournament = EliminationTournament(
            players=players,
            location="Brno",
            winning_score=10,
            max_dice_value=6
        )
        
        print(f"Vytvoreno: {tournament}")
        print(f"Typ turnaje: {tournament._get_tournament_type_name()}")
        print(f"Ocekavany pocet kol: {tournament._get_total_rounds()}")
        
        # Krátký turnaj
        tournament.winning_score = 3
        
        tournament.play()
        tournament.print_standings()
        
        print(f"\nVítěz: {tournament.winner.nickname if tournament.winner else 'None'}")
        print(f"Počet zápasů: {len(tournament.matches)}")
        print(f"Počet detailů: {len(tournament._detailed_results)}")
        
        print("\nOK - Eliminacni test byl uspesny!")
        return True
        
    except Exception as e:
        print(f"\nCHYBA - Chyba při testu: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_polymorphism():
    """Testuje polymorfismus přes abstraktní třídu."""
    print("\n" + "="*70)
    print("TEST 3: Polymorfismus")
    print("="*70)
    
    try:
        players = load_players("players.json")
        
        if len(players) < 4:
            print(f"Nedostatek hracu: {len(players)}")
            return False
        
        # Rozdělíme hráče
        players_rr = players[:len(players)//2]
        players_elim = players[len(players)//2:]
        
        tournaments = [
            RoundRobinTournament(players_rr, "Praha", winning_score=2),
            EliminationTournament(players_elim, "Brno", winning_score=2)
        ]
        
        print(f"Vytvořeno {len(tournaments)} turnajů")
        
        for i, tournament in enumerate(tournaments, 1):
            print(f"\n  Turnaj {i}:")
            print(f"    - Třída: {tournament.__class__.__name__}")
            print(f"    - Typ: {tournament._get_tournament_type_name()}")
            print(f"    - Kol: {tournament._get_total_rounds()}")
            print(f"    - Hráči: {[p.nickname for p in tournament.players]}")
        
        print("\nOK - Test polymorfismu byl uspesny!")
        return True
        
    except Exception as e:
        print(f"\nCHYBA - Chyba při testu: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_factory():
    """Testuje TournamentFactory."""
    print("\n" + "="*70)
    print("TEST 4: TournamentFactory")
    print("="*70)
    
    try:
        players = load_players("players.json")
        
        if len(players) < 2:
            print(f"Nedostatek hracu: {len(players)}")
            return False
        
        # Test vytvoření pomocí Factory
        print("\nDostupné typy turnajů:")
        types = TournamentFactory.get_available_types()
        for t in types:
            print(f"  - {t}")
        
        # Vytvoř oba typy
        tournaments = []
        for tournament_type in types:
            t = TournamentFactory.create(
                tournament_type=tournament_type,
                players=players,
                location="Ostrava",
                winning_score=2
            )
            tournaments.append((tournament_type, t))
            print(f"\nVytvořeno pomocí Factory: {tournament_type}")
            print(f"  Třída: {t.__class__.__name__}")
            print(f"  Typ: {t._get_tournament_type_name()}")
        
        # Test neexistujícího typu
        try:
            TournamentFactory.create("neexistujici", players, "Praha")
            print("\nCHYBA - Factory měla vyhodit ValueError!")
            return False
        except ValueError as e:
            print(f"\nOK - Očekávaná výjimka: {e}")
        
        print("\nOK - Test TournamentFactory byl uspesny!")
        return True
        
    except Exception as e:
        print(f"\nCHYBA - Chyba při testu: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Spustí všechny testy."""
    print("\n" + "="*70)
    print("TESTY - Abstraktní turnaje (tournament_abc)")
    print("="*70)
    
    results = []
    
    # Test 1
    result1 = test_round_robin()
    results.append(("Round-robin", result1))
    
    # Test 2
    result2 = test_elimination()
    results.append(("Eliminace", result2))
    
    # Test 3
    result3 = test_polymorphism()
    results.append(("Polymorfismus", result3))
    
    # Test 4
    result4 = test_factory()
    results.append(("TournamentFactory", result4))
    
    # Shrnutí
    print("\n" + "="*70)
    print("VYSLEDKY TESTU")
    print("="*70)
    
    for name, result in results:
        status = "OK" if result else "CHYBA"
        print(f"{name:<20} ... {status}")
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    print(f"\nUspechost: {passed}/{total}")
    
    if passed == total:
        print("\nVšechny testy PROSLY!")
    else:
        print(f"\n{total - passed} test(y) SELHALY!")


if __name__ == "__main__":
    main()
