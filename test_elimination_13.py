"""Test eliminačního turnaje se 13 hráči."""

from game import load_players
from tournament_abc import TournamentFactory

# Načti hráče
players = load_players("players.json")

print(f"Načteno {len(players)} hráčů")

# Vytvoř eliminační turnaj
tournament = TournamentFactory.create(
    "elimination",
    players,
    "Praha",
    winning_score=3,  # Krátké zápasy pro rychlý test
    max_dice_value=6
)

print(f"\n=== TEST: Eliminační turnaj se {len(players)} hráči ===\n")
print("Očekávaná struktura:")
print(f"  - {len(players)} hráčů celkem")

import math
next_power = 2 ** math.ceil(math.log2(len(players)))
num_byes = len(players) - (len(players) - next_power // 2) * 2

print(f"  - Nejbližší mocnina 2: {next_power}")
print(f"  - Hráči s volným losem: {num_byes}")
print(f"  - Hráči v prvním kole: {len(players) - num_byes}")
print(f"  - První kolo zápasů: {(len(players) - num_byes) // 2}")

# Spusť turnaj
tournament.play()

print(f"\n=== VÍTĚZ: {tournament.winner.nickname} ===")
print(f"Celkem odehráno zápasů: {len(tournament.matches)}")
