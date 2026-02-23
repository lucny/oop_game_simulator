"""Alternativní modul pro turnaje s abstraktní třídou a dědičností.

Demonstruje abstraktní dědičnost (ABC - Abstract Base Classes):
- BaseTournament - abstraktní bázová třída
- RoundRobinTournament - konkrétní implementace round-robin turnaje
- EliminationTournament - konkrétní implementace eliminačního turnaje
- TournamentPrinter - pomocná třída pro výstupní zprávy
- TournamentFactory - tovární třída pro vytváření turnajů

Výhody tohoto přístupu:
- Čistější oddělení kódu dle typu turnaje
- Jednoduší rozšíření o nové typy turnajů
- Polymorfismus přes abstraktní metody
- Vynucení implementace abstraktních metod
- Separace výstupní logiky (Single Responsibility Principle)
- Factory pattern pro snadné vytváření instancí
"""

import datetime
import math
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Tuple
from game import Player, Match
from files import jsonfile_write


class TournamentPrinter:
    """Pomocná třída pro formátované výstupy turnaje.
    
    Zajišťuje konzistentní formátování napříč všemi typy turnajů
    a odděluje výstupní logiku od business logiky turnaje.
    """

    @staticmethod
    def print_separator(width: int = 70, char: str = '='):
        """Vytiskne oddělovač.
        
        Args:
            width (int): Šířka oddělovače.
            char (str): Znak pro oddělovač.
        """
        print(char * width)

    @staticmethod
    def print_tournament_header(tournament_type: str, location: str, num_players: int):
        """Vytiskne záhlaví turnaje.
        
        Args:
            tournament_type (str): Typ turnaje (např. "Každý s každým").
            location (str): Místo konání.
            num_players (int): Počet hráčů.
        """
        TournamentPrinter.print_separator()
        print(f"TURNAJ: {tournament_type}")
        print(f"Místo: {location}")
        print(f"Počet hráčů: {num_players}")
        TournamentPrinter.print_separator()
        print()

    @staticmethod
    def print_round_header(round_info: str):
        """Vytiskne záhlaví kola.
        
        Args:
            round_info (str): Informace o kole (např. "KOLO 1", "FINÁLE").
        """
        print()
        TournamentPrinter.print_separator()
        print(round_info)
        TournamentPrinter.print_separator()

    @staticmethod
    def print_match_info(player1_name: str, player2_name: str):
        """Vytiskne informace o nadcházejícím zápase.
        
        Args:
            player1_name (str): Jméno prvního hráče.
            player2_name (str): Jméno druhého hráče.
        """
        print(f"\nZápas: {player1_name} vs {player2_name}")

    @staticmethod
    def print_match_result(player1_name: str, player2_name: str, 
                          score1: int, score2: int, winner_name: str,
                          additional_info: str = ""):
        """Vytiskne výsledek zápasu.
        
        Args:
            player1_name (str): Jméno prvního hráče.
            player2_name (str): Jméno druhého hráče.
            score1 (int): Skóre prvního hráče.
            score2 (int): Skóre druhého hráče.
            winner_name (str): Jméno vítěze.
            additional_info (str): Dodatečné informace (např. "Vyřazen: X").
        """
        print(f"Výsledek: {player1_name} {score1} - {score2} {player2_name}")
        print(f"Vítěz: {winner_name}")
        if additional_info:
            print(additional_info)

    @staticmethod
    def print_elimination_result(winner_name: str, loser_name: str):
        """Vytiskne výsledek eliminačního zápasu.
        
        Args:
            winner_name (str): Jméno postupujícího hráče.
            loser_name (str): Jméno vyřazeného hráče.
        """
        print(f"Postupuje: {winner_name} | Vyřazen: {loser_name}")

    @staticmethod
    def print_bye_info(player_name: str):
        """Vytiskne informaci o automatickém postupu.
        
        Args:
            player_name (str): Jméno hráče s volným losem.
        """
        print(f"\n{player_name} postupuje automaticky (lichý počet hráčů)\n")

    @staticmethod
    def print_winner(winner_name: str, additional_stats: str = ""):
        """Vytiskne informaci o vítězi turnaje.
        
        Args:
            winner_name (str): Jméno vítěze.
            additional_stats (str): Dodatečné statistiky.
        """
        print()
        TournamentPrinter.print_separator()
        print(f"VITEZ TURNAJE: {winner_name}")
        if additional_stats:
            print(additional_stats)
        TournamentPrinter.print_separator()
        print()

    @staticmethod
    def print_current_standings(standings: List[Tuple], max_display: int = 5):
        """Vytiskne průběžné pořadí.
        
        Args:
            standings (List[Tuple]): Seznam tuple (hráč, výhry, skóre_rozdíl).
            max_display (int): Maximální počet zobrazených hráčů.
        """
        for idx, (player, wins, score_diff) in enumerate(standings[:max_display], 1):
            print(f"  {idx}. {player.nickname}: {wins} výher, "
                  f"skóre +{player.score['plus']} -{player.score['minus']}")

    @staticmethod
    def print_round_standings(round_num: int, standings: List[Tuple]):
        """Vytiskne stav po kole.
        
        Args:
            round_num (int): Číslo kola.
            standings (List[Tuple]): Seznam tuple (hráč, výhry, skóre_rozdíl).
        """
        print(f"\n{'-'*70}")
        print(f"Stav po kole {round_num}:")
        TournamentPrinter.print_current_standings(standings)

    @staticmethod
    def print_final_standings(standings: List[Tuple]):
        """Vytiskne konečné pořadí.
        
        Args:
            standings (List[Tuple]): Seznam tuple (hráč, výhry, skóre_rozdíl).
        """
        print()
        TournamentPrinter.print_separator(80)
        print("KONEČNÉ POŘADÍ")
        TournamentPrinter.print_separator(80)
        print(f"{'Poř.':<6} {'Hráč':<20} {'Stát':<10} {'Výhry':<8} {'Zápasy':<8} "
              f"{'Skóre':<15} {'Úspěšnost':<10}")
        print('-' * 80)

        for idx, (player, wins, score_diff) in enumerate(standings, 1):
            score_str = f"+{player.score['plus']} -{player.score['minus']}"
            win_rate = player.win_rate()
            print(f"{idx:<6} {player.nickname:<20} {player.state:<10} {wins:<8} "
                  f"{player.count_of_games:<8} {score_str:<15} {win_rate}%")

        TournamentPrinter.print_separator(80)
        print()

    @staticmethod
    def print_save_confirmation(filename: str):
        """Vytiskne potvrzení o uložení.
        
        Args:
            filename (str): Název souboru.
        """
        print(f"✓ Detailní výsledky turnaje uloženy do '{filename}'")


class TournamentFactory:
    """Tovární třída pro vytváření instancí turnajů.
    
    Implementuje Factory pattern pro snadné a čisté vytváření
    různých typů turnajů bez nutnosti přímé práce s konkrétními třídami.
    """

    @staticmethod
    def create(tournament_type: str, players: List[Player], location: str,
               winning_score: int = 10, max_dice_value: int = 6) -> 'BaseTournament':
        """Vytvoří instanci turnaje podle typu.
        
        Args:
            tournament_type (str): Typ turnaje ("round_robin" nebo "elimination").
            players (List[Player]): Seznam hráčů.
            location (str): Místo konání turnaje.
            winning_score (int): Počet bodů k vítězství v zápase.
            max_dice_value (int): Maximální hodnota kostky.
            
        Returns:
            BaseTournament: Instance konkrétního typu turnaje.
            
        Raises:
            ValueError: Pokud je zadán neznámý typ turnaje.
            
        Example:
            >>> players = load_players("players.json")
            >>> tournament = TournamentFactory.create("round_robin", players, "Praha")
            >>> tournament.play()
        """
        tournament_type = tournament_type.lower().strip()
        
        if tournament_type == "round_robin":
            return RoundRobinTournament(players, location, winning_score, max_dice_value)
        elif tournament_type == "elimination":
            return EliminationTournament(players, location, winning_score, max_dice_value)
        else:
            raise ValueError(
                f"Neznámý typ turnaje: '{tournament_type}'. "
                f"Podporované typy: 'round_robin', 'elimination'"
            )

    @staticmethod
    def get_available_types() -> List[str]:
        """Vrací seznam dostupných typů turnajů.
        
        Returns:
            List[str]: Seznam názvů typů turnajů.
        """
        return ["round_robin", "elimination"]


class BaseTournament(ABC):
    """Abstraktní bázová třída pro všechny typy turnajů.

    Definuje společné atributy a abstraktní metody, které musí být
    implementovány v podtřídách.
    """

    def __init__(self, players: List[Player], location: str,
                 winning_score: int = 10, max_dice_value: int = 6):
        """Inicializuje základní data turnaje.

        Args:
            players (List[Player]): Seznam hráčů účastnících se turnaje.
            location (str): Místo konání turnaje.
            winning_score (int): Počet bodů k vítězství v jednom zápase (výchozí: 10).
            max_dice_value (int): Maximální hodnota kostky (výchozí: 6).

        Raises:
            ValueError: Pokud je málo hráčů nebo chybí místo konání.
        """
        if len(players) < 2:
            raise ValueError("Turnaj vyžaduje alespoň 2 hráče.")

        if not location or not location.strip():
            raise ValueError("Místo konání turnaje musí být zadáno.")

        self.players = players
        self.location = location.strip()
        self.winning_score = winning_score
        self.max_dice_value = max_dice_value
        self._datetime = datetime.datetime.now()
        self.matches: List[Match] = []
        self.winner: Optional[Player] = None
        self._detailed_results: List[Dict] = []

    def __str__(self):
        """Vrací textovou reprezentaci turnaje."""
        player_names = ', '.join([p.nickname for p in self.players])
        tournament_type = self.__class__.__name__
        return f"{tournament_type} v {self.location}: {player_names}"

    @abstractmethod
    def play(self):
        """Abstraktní metoda pro odehrání turnaje.

        Musí být implementována v podtřídách.
        """
        pass

    @abstractmethod
    def _print_tournament_header(self):
        """Abstraktní metoda pro tisk záhlaví turnaje."""
        pass

    def get_standings(self) -> List[Tuple[Player, int, int]]:
        """Vrací pořadí hráčů v turnaji.

        Returns:
            List[Tuple[Player, int, int]]: Seznam tuple (hráč, výhry, skóre_rozdíl) seřazený podle výher.
        """
        standings = []
        for player in self.players:
            score_diff = player.score['plus'] - player.score['minus']
            standings.append((player, player.wins, score_diff))

        standings.sort(key=lambda x: (x[1], x[2]), reverse=True)
        return standings

    def print_standings(self):
        """Vytiskne tabulku s konečným pořadím hráčů."""
        standings = self.get_standings()
        TournamentPrinter.print_final_standings(standings)

    def save_tournament_results(self, filename: str = "tournament_results.json"):
        """Uloží detailní výsledky turnaje do JSON souboru.

        Args:
            filename (str): Název souboru pro uložení (výchozí: tournament_results.json).

        Raises:
            IOError: Pokud došlo k chybě při ukládání.
        """
        try:
            tournament_data = {
                "tournament_info": {
                    "date": self._datetime.strftime("%Y-%m-%d %H:%M:%S"),
                    "location": self.location,
                    "type": self._get_tournament_type_name(),
                    "winning_score": self.winning_score,
                    "max_dice_value": self.max_dice_value
                },
                "players": [
                    {
                        "nickname": p.nickname,
                        "state": p.state,
                        "gender": p.gender.value
                    }
                    for p in self.players
                ],
                "winner": {
                    "nickname": self.winner.nickname,
                    "state": self.winner.state,
                    "total_wins": self.winner.wins,
                    "total_games": self.winner.count_of_games,
                    "win_rate": self.winner.win_rate()
                } if self.winner else None,
                "matches": self._detailed_results,
                "final_standings": [
                    {
                        "position": idx,
                        "player": player.nickname,
                        "state": player.state,
                        "wins": wins,
                        "games": player.count_of_games,
                        "score_plus": player.score['plus'],
                        "score_minus": player.score['minus'],
                        "score_difference": player.score['plus'] - player.score['minus'],
                        "win_rate": player.win_rate()
                    }
                    for idx, (player, wins, _) in enumerate(self.get_standings(), 1)
                ],
                "statistics": {
                    "total_matches": len(self.matches),
                    "total_rounds": self._get_total_rounds(),
                    "average_match_duration": sum(m['match_duration'] for m in self._detailed_results) / len(self._detailed_results)
                                              if self._detailed_results else 0
                }
            }

            jsonfile_write(filename, tournament_data)
            TournamentPrinter.print_save_confirmation(filename)
        except Exception as e:
            raise IOError(f"Chyba při ukládání výsledků turnaje: {e}")

    @abstractmethod
    def _get_tournament_type_name(self) -> str:
        """Vrací název typu turnaje.

        Returns:
            str: Název turnaje (např. "round_robin", "elimination").
        """
        pass

    @abstractmethod
    def _get_total_rounds(self) -> int:
        """Vrací celkový počet kol.

        Returns:
            int: Počet kol v turnaji.
        """
        pass


class RoundRobinTournament(BaseTournament):
    """Třída pro turnaj formou 'každý s každým' organizovaný do kol."""

    def play(self):
        """Odehraje turnaj ve formátu každý s každým organizovaný do kol."""
        self._print_tournament_header()

        schedule = self._generate_round_robin_schedule()

        for round_num, round_matches in enumerate(schedule, 1):
            TournamentPrinter.print_round_header(f"KOLO {round_num}")

            for player1, player2 in round_matches:
                TournamentPrinter.print_match_info(player1.nickname, player2.nickname)
                match = Match(player1, player2, self.winning_score, self.max_dice_value)
                match.play()
                self.matches.append(match)

                score = match.score()
                winner = player1 if score[0] > score[1] else player2
                TournamentPrinter.print_match_result(
                    player1.nickname, player2.nickname, score[0], score[1], winner.nickname
                )

                # Uložení detailních informací o zápasu
                self._detailed_results.append({
                    "round": round_num,
                    "match_type": "round_robin",
                    "player1": {
                        "nickname": player1.nickname,
                        "state": player1.state
                    },
                    "player2": {
                        "nickname": player2.nickname,
                        "state": player2.state
                    },
                    "final_score": {
                        "player1": score[0],
                        "player2": score[1]
                    },
                    "winner": winner.nickname,
                    "score_history": match.get_history(),
                    "match_duration": len(match.get_history())
                })

            # Mezivýsledky po každém kole
            TournamentPrinter.print_round_standings(round_num, self.get_standings())

        self._determine_winner()

    def _print_tournament_header(self):
        """Vytiskne záhlaví pro turnaj 'každý s každým'."""
        TournamentPrinter.print_tournament_header(
            "Každý s každým", self.location, len(self.players)
        )

    def _generate_round_robin_schedule(self) -> List[List[Tuple[Player, Player]]]:
        """Generuje rozvrh pro turnaj každý s každým rozdělený do kol.

        Používá Round-robin algoritmus, kde každý hráč hraje v každém kole max. jednou.

        Returns:
            List[List[Tuple[Player, Player]]]: Seznam kol, každé kolo obsahuje páry hráčů.
        """
        players = self.players.copy()
        n = len(players)

        # Pokud je lichý počet hráčů, přidáme "BYE" (volno)
        if n % 2 != 0:
            players.append(None)
            n += 1

        rounds = []

        # Round-robin algoritmus: generování n-1 kol
        for round_num in range(n - 1):
            round_matches = []

            for i in range(n // 2):
                player1 = players[i]
                player2 = players[n - 1 - i]

                # Přeskočit zápasy s None (BYE)
                if player1 is not None and player2 is not None:
                    round_matches.append((player1, player2))

            rounds.append(round_matches)

            # Rotace hráčů (první zůstává, ostatní rotují)
            players = [players[0]] + [players[-1]] + players[1:-1]

        return rounds

    def _determine_winner(self):
        """Určí vítěze turnaje podle počtu výher."""
        max_wins = max(player.wins for player in self.players)
        winners = [player for player in self.players if player.wins == max_wins]

        if len(winners) == 1:
            self.winner = winners[0]
        else:
            # Remíza - vybere hráče s lepším skóre
            self.winner = max(winners, key=lambda p: p.score['plus'] - p.score['minus'])

        stats = f"Výhry: {self.winner.wins}, Skóre: +{self.winner.score['plus']} -{self.winner.score['minus']}"
        TournamentPrinter.print_winner(self.winner.nickname, stats)

    def _get_tournament_type_name(self) -> str:
        """Vrací název typu turnaje."""
        return "round_robin"

    def _get_total_rounds(self) -> int:
        """Vrací počet kol v turnaji."""
        n = len(self.players)
        return n - 1 if n % 2 == 0 else n


class EliminationTournament(BaseTournament):
    """Třída pro turnaj v eliminačním formátu (vyřazovací systém/pavouk)."""

    def play(self):
        """Odehraje turnaj v eliminačním formátu (pavouk).
        
        Správně řeší strukturu pavouka pro libovolný počet hráčů:
        - Vypočítá počet hráčů s volným losem (bye)
        - Bye hráči postupují přímo do dalšího kola
        - Ostatní hrají první kolo
        """
        self._print_tournament_header()

        remaining_players = self.players.copy()
        round_num = 1
        
        # Inicializace proměnných
        bye_players = []
        first_round = True

        # První kolo - vypočítat bye hráče
        num_byes = self._calculate_byes(len(remaining_players))
        
        if num_byes > 0:
            TournamentPrinter.print_round_header("VOLNÉ LOSY")
            bye_players = remaining_players[:num_byes]
            playing_players = remaining_players[num_byes:]
            
            for bye_player in bye_players:
                TournamentPrinter.print_bye_info(bye_player.nickname)
            
            remaining_players = playing_players

        # Hlavní smyčka turnaje
        while len(remaining_players) > 1 or (first_round and bye_players):
            # Počet hráčů, kteří budou hrát
            num_playing = len(remaining_players)
            
            # Název kola závisí na celkovém počtu v tomto kole
            if first_round and bye_players:
                total_in_round = num_playing + len(bye_players)
            else:
                total_in_round = num_playing
            
            round_name = self._get_elimination_round_name(total_in_round)
            TournamentPrinter.print_round_header(round_name)
            
            next_round_players = []
            
            # Odehrát zápasy
            for i in range(0, len(remaining_players), 2):
                if i + 1 >= len(remaining_players):
                    # Lichý hráč - volný los v tomto kole
                    bye_player = remaining_players[i]
                    TournamentPrinter.print_bye_info(bye_player.nickname)
                    next_round_players.append(bye_player)
                    break
                
                player1 = remaining_players[i]
                player2 = remaining_players[i + 1]

                TournamentPrinter.print_match_info(player1.nickname, player2.nickname)
                match = Match(player1, player2, self.winning_score, self.max_dice_value)
                match.play()
                self.matches.append(match)

                score = match.score()
                winner = player1 if score[0] > score[1] else player2
                loser = player2 if winner == player1 else player1

                TournamentPrinter.print_match_result(
                    player1.nickname, player2.nickname, score[0], score[1], winner.nickname
                )
                TournamentPrinter.print_elimination_result(winner.nickname, loser.nickname)

                next_round_players.append(winner)

                # Uložení detailních informací o zápasu
                self._detailed_results.append({
                    "round": round_num,
                    "round_name": round_name,
                    "match_type": "elimination",
                    "player1": {
                        "nickname": player1.nickname,
                        "state": player1.state
                    },
                    "player2": {
                        "nickname": player2.nickname,
                        "state": player2.state
                    },
                    "final_score": {
                        "player1": score[0],
                        "player2": score[1]
                    },
                    "winner": winner.nickname,
                    "eliminated": loser.nickname,
                    "score_history": match.get_history(),
                    "match_duration": len(match.get_history())
                })
            
            # Přidat bye hráče z prvního kola - PROKLÁDAT s vítězi
            if first_round and bye_players:
                # Prokládat nasazené (bye) s nenasazenými (vítězi prvního kola)
                combined = []
                max_len = max(len(next_round_players), len(bye_players))
                
                for i in range(max_len):
                    # Přidat vítěze z prvního kola
                    if i < len(next_round_players):
                        combined.append(next_round_players[i])
                    # Přidat nasazeného hráče
                    if i < len(bye_players):
                        combined.append(bye_players[i])
                
                next_round_players = combined
                first_round = False

            remaining_players = next_round_players
            round_num += 1
        
        # Kontrola, že máme právě jednoho vítěze
        if len(remaining_players) == 1:
            self.winner = remaining_players[0]
        else:
            # Fallback - vybrat prvního
            self.winner = remaining_players[0] if remaining_players else self.players[0]
        
        TournamentPrinter.print_winner(self.winner.nickname)

    def _calculate_byes(self, num_players: int) -> int:
        """Vypočítá počet hráčů s volným losem (bye) v prvním kole.
        
        Pro správnou strukturu pavouka:
        - Najde nejbližší vyšší mocninu dvojky
        - Vrátí rozdíl = počet bye hráčů
        
        Args:
            num_players (int): Celkový počet hráčů.
            
        Returns:
            int: Počet hráčů s volným losem.
            
        Example:
            13 hráčů → nejbližší mocnina = 16 → 3 bye (13 - 10 = 3)
            10 hráčů → 10 hraje osmifinále, 3 má bye do čtvrtfinále
        """
        if num_players <= 1:
            return 0
        
        # Najdi nejbližší vyšší mocninu dvojky
        import math
        next_power = 2 ** math.ceil(math.log2(num_players))
        
        # Počet zápasů v prvním kole
        num_matches_first_round = num_players - next_power // 2
        
        # Počet bye = hráči, kteří nehrají první kolo
        num_byes = num_players - (num_matches_first_round * 2)
        
        return num_byes

    def _print_tournament_header(self):
        """Vytiskne záhlaví pro eliminační turnaj."""
        TournamentPrinter.print_tournament_header(
            "Eliminační systém", self.location, len(self.players)
        )

    def _get_elimination_round_name(self, num_players: int) -> str:
        """Vrací název kola podle počtu zbývajících hráčů.

        Args:
            num_players (int): Počet zbývajících hráčů.

        Returns:
            str: Název kola (např. "FINÁLE", "SEMIFINÁLE").
        """
        if num_players == 2:
            return "FINÁLE"
        elif num_players == 4:
            return "SEMIFINÁLE"
        elif num_players == 8:
            return "ČTVRTFINÁLE"
        elif num_players == 16:
            return "OSMIFINÁLE"
        else:
            return f"KOLO {num_players} HRÁČŮ"

    def _get_tournament_type_name(self) -> str:
        """Vrací název typu turnaje."""
        return "elimination"

    def _get_total_rounds(self) -> int:
        """Vrací počet kol v eliminačním turnaji."""
        n = len(self.players)
        # Počet kol = log₂(n) zaokrouhleno nahoru
        import math
        return math.ceil(math.log2(n)) if n > 0 else 0
