"""Vylepšený modul pro organizaci a simulaci turnajů mezi hráči.

Obsahuje třídu Tournament s pokročilými funkcemi:
- Místo konání turnaje
- Round-robin s koly (každý tým hraje v každém kole)
- Detailní záznamy zápasů včetně vývoje skóre
"""

import datetime
from enum import Enum
from typing import List, Optional, Dict, Tuple, Set
from game import Player, Match
from files import jsonfile_write


class TournamentType(Enum):
    """Výčtový typ pro typy turnajů."""
    ROUND_ROBIN = "round_robin"
    ELIMINATION = "elimination"


class Tournament:
    """Třída reprezentující turnaj mezi více hráči s pokročilými funkcemi."""

    def __init__(self, players: List[Player], location: str,
                 tournament_type: TournamentType = TournamentType.ROUND_ROBIN,
                 winning_score: int = 10, max_dice_value: int = 6):
        """Inicializuje turnaj.

        Args:
            players (List[Player]): Seznam hráčů účastnících se turnaje.
            location (str): Místo konání turnaje.
            tournament_type (TournamentType): Typ turnaje (výchozí: ROUND_ROBIN).
            winning_score (int): Počet bodů k vítězství v jednom zápase (výchozí: 10).
            max_dice_value (int): Maximální hodnota kostky (výchozí: 6).

        Raises:
            ValueError: Pokud je málo hráčů nebo chybí místo konání.
        """
        if len(players) < 2:
            raise ValueError("Turnaj vyžaduje alespoň 2 hráče.")
        
        if not location or not location.strip():
            raise ValueError("Místo konání turnaje musí být zadáno.")
        
        if tournament_type == TournamentType.ELIMINATION and len(players) < 2:
            raise ValueError("Eliminační turnaj vyžaduje alespoň 2 hráče.")
        
        self.players = players
        self.location = location.strip()
        self.tournament_type = tournament_type
        self.winning_score = winning_score
        self.max_dice_value = max_dice_value
        self._datetime = datetime.datetime.now()
        self.matches: List[Match] = []
        self.winner: Optional[Player] = None
        self._detailed_results: List[Dict] = []

    def __str__(self):
        """Vrací textovou reprezentaci turnaje."""
        player_names = ', '.join([p.nickname for p in self.players])
        return f"Turnaj v {self.location} ({self.tournament_type.value}): {player_names}"

    def play(self):
        """Odehraje turnaj podle zvoleného typu.

        Raises:
            ValueError: Pokud není nastaven platný typ turnaje.
        """
        if self.tournament_type == TournamentType.ROUND_ROBIN:
            self._play_round_robin()
        elif self.tournament_type == TournamentType.ELIMINATION:
            self._play_elimination()
        else:
            raise ValueError(f"Neznámý typ turnaje: {self.tournament_type}")

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

    def _play_round_robin(self):
        """Odehraje turnaj ve formátu každý s každým organizovaný do kol."""
        print(f"\n{'='*70}")
        print(f"TURNAJ: Každý s každým")
        print(f"Místo: {self.location}")
        print(f"Počet hráčů: {len(self.players)}")
        print(f"{'='*70}\n")

        schedule = self._generate_round_robin_schedule()
        
        for round_num, round_matches in enumerate(schedule, 1):
            print(f"\n{'='*70}")
            print(f"KOLO {round_num}")
            print(f"{'='*70}")
            
            for player1, player2 in round_matches:
                print(f"\nZápas: {player1.nickname} vs {player2.nickname}")
                match = Match(player1, player2, self.winning_score, self.max_dice_value)
                match.play()
                self.matches.append(match)

                score = match.score()
                winner = player1 if score[0] > score[1] else player2
                print(f"Výsledek: {player1.nickname} {score[0]} - {score[1]} {player2.nickname}")
                print(f"Vítěz: {winner.nickname}")
                
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
            print(f"\n{'-'*70}")
            print(f"Stav po kole {round_num}:")
            self._print_current_standings()

        self._determine_round_robin_winner()

    def _play_elimination(self):
        """Odehraje turnaj v eliminačním formátu (pavouk)."""
        print(f"\n{'='*70}")
        print(f"TURNAJ: Eliminační systém")
        print(f"Místo: {self.location}")
        print(f"Počet hráčů: {len(self.players)}")
        print(f"{'='*70}\n")

        remaining_players = self.players.copy()
        round_num = 1

        while len(remaining_players) > 1:
            round_name = self._get_elimination_round_name(len(remaining_players))
            print(f"\n{'='*70}")
            print(f"{round_name}")
            print(f"{'='*70}")
            
            if len(remaining_players) % 2 != 0:
                bye_player = remaining_players[0]
                print(f"\n{bye_player.nickname} postupuje automaticky (lichý počet hráčů)\n")
                remaining_players = remaining_players[1:]
                next_round_players = [bye_player]
            else:
                next_round_players = []

            for i in range(0, len(remaining_players), 2):
                player1 = remaining_players[i]
                player2 = remaining_players[i + 1]

                print(f"\nZápas: {player1.nickname} vs {player2.nickname}")
                match = Match(player1, player2, self.winning_score, self.max_dice_value)
                match.play()
                self.matches.append(match)

                score = match.score()
                winner = player1 if score[0] > score[1] else player2
                loser = player2 if winner == player1 else player1
                
                print(f"Výsledek: {player1.nickname} {score[0]} - {score[1]} {player2.nickname}")
                print(f"Postupuje: {winner.nickname} | Vyřazen: {loser.nickname}")

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

            remaining_players = next_round_players
            round_num += 1

        self.winner = remaining_players[0]
        print(f"\n{'='*70}")
        print(f"🏆 VÍTĚZ TURNAJE: {self.winner.nickname} 🏆")
        print(f"{'='*70}\n")

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

    def _determine_round_robin_winner(self):
        """Určí vítěze turnaje každý s každým podle počtu výher."""
        max_wins = max(player.wins for player in self.players)
        winners = [player for player in self.players if player.wins == max_wins]

        if len(winners) == 1:
            self.winner = winners[0]
        else:
            # Remíza - vybere hráče s lepším skóre
            self.winner = max(winners, key=lambda p: p.score['plus'] - p.score['minus'])

        print(f"\n{'='*70}")
        print(f"🏆 VÍTĚZ TURNAJE: {self.winner.nickname} 🏆")
        print(f"Výhry: {self.winner.wins}, Skóre: +{self.winner.score['plus']} -{self.winner.score['minus']}")
        print(f"{'='*70}\n")

    def _print_current_standings(self):
        """Vytiskne aktuální průběžné pořadí."""
        standings = self.get_standings()
        for idx, (player, wins, score_diff) in enumerate(standings[:5], 1):
            print(f"  {idx}. {player.nickname}: {wins} výher, "
                  f"skóre +{player.score['plus']} -{player.score['minus']}")

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
        print(f"\n{'='*80}")
        print("KONEČNÉ POŘADÍ")
        print(f"{'='*80}")
        print(f"{'Poř.':<6} {'Hráč':<20} {'Stát':<10} {'Výhry':<8} {'Zápasy':<8} "
              f"{'Skóre':<15} {'Úspěšnost':<10}")
        print(f"{'-'*80}")

        standings = self.get_standings()
        for idx, (player, wins, score_diff) in enumerate(standings, 1):
            score_str = f"+{player.score['plus']} -{player.score['minus']}"
            win_rate = player.win_rate()
            print(f"{idx:<6} {player.nickname:<20} {player.state:<10} {wins:<8} "
                  f"{player.count_of_games:<8} {score_str:<15} {win_rate}%")
        
        print(f"{'='*80}\n")

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
                    "type": self.tournament_type.value,
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
                    "total_rounds": len(self._detailed_results) if self.tournament_type == TournamentType.ROUND_ROBIN 
                                    else max([m['round'] for m in self._detailed_results]) if self._detailed_results else 0,
                    "average_match_duration": sum(m['match_duration'] for m in self._detailed_results) / len(self._detailed_results)
                                              if self._detailed_results else 0
                }
            }

            jsonfile_write(filename, tournament_data)
            print(f"✓ Detailní výsledky turnaje uloženy do '{filename}'")
        except Exception as e:
            raise IOError(f"Chyba při ukládání výsledků turnaje: {e}")
