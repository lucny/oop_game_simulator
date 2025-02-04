import datetime
from enum import Enum
from random import randrange
from files import jsonfile_read, jsonfile_write


class Gender(Enum):
    """Výčtový typ pro pohlaví"""
    male = 'man'
    female = 'woman'


class Dice:
    """Třída simulující hod kostkou s nastavitelným rozsahem hodnot"""
    @staticmethod
    def roll(max_value=6):
        if max_value < 4 or max_value > 9:
            raise ValueError("Maximální hodnota musí být v rozmezí 4 až 9.")
        return randrange(1, max_value + 1)


class Person:
    def __init__(self, nickname: str, gender: Gender):
        self.nickname = nickname
        self.gender = gender
        self._birth = datetime.datetime.now()

    def __str__(self):
        return f'Nickname: {self.nickname}, gender: {self.gender.value}'

    @property
    def gender(self):
        return self._gender

    @gender.setter
    def gender(self, gender):
        if isinstance(gender, Gender):
            self._gender = gender
        else:
            raise ValueError("Gender value not valid")

    def get_seconds_from_birth(self):
        return int((datetime.datetime.now() - self._birth).total_seconds())


class Player(Person):
    def __init__(self, nickname: str, gender: Gender, state: str):
        super().__init__(nickname, gender)
        self.state = state
        self.count_of_games = 0
        self.wins = 0
        self.score = {'plus': 0, 'minus': 0}

    def __str__(self):
        return f'{super().__str__()}, state: {self.state}'

    @property
    def wins(self):
        return self._wins

    @wins.setter
    def wins(self, value):
        if value < 0:
            raise ValueError("Property wins must not be a negative value")
        self._wins = value

    def win_rate(self):
        return round(self.wins / self.count_of_games * 100, 2) if self.count_of_games > 0 else 0.0
    
    def overall_score(self):
        return self.score["plus"], self.score["minus"]


class Match:
    def __init__(self, house_player: Player, guest_player: Player, winning_score=10, max_dice_value=6):
        self.h_player = house_player
        self.g_player = guest_player
        self.winning_score = winning_score
        self.max_dice_value = max_dice_value
        self._datetime = datetime.datetime.now()
        self.hp_points = 0
        self.gp_points = 0
        self._history = []

    def __str__(self):
        return f'{self.h_player.nickname} vs. {self.g_player.nickname} {self.score()}'

    @property
    def h_player(self):
        return self._hplayer

    @h_player.setter
    def h_player(self, player):
        if isinstance(player, Player):
            self._hplayer = player
        else:
            raise TypeError("h_player must be instance of Player")

    @property
    def g_player(self):
        return self._gplayer

    @g_player.setter
    def g_player(self, player):
        if isinstance(player, Player):
            self._gplayer = player
        else:
            raise TypeError("g_player must be instance of Player")

    def __roll(self):
        while True:
            hp = Dice.roll(self.max_dice_value)
            gp = Dice.roll(self.max_dice_value)
            if hp != gp:
                break
        return 0 if hp > gp else 1

    def play(self):
        while self.hp_points < self.winning_score and self.gp_points < self.winning_score:
            if self.__roll() == 0:
                self.hp_points += 1
            else:
                self.gp_points += 1
            self._history.append(self.score())
        
        self.h_player.count_of_games += 1
        self.g_player.count_of_games += 1

        self.h_player.score['plus'] += self.hp_points
        self.h_player.score['minus'] += self.gp_points
        self.g_player.score['plus'] += self.gp_points
        self.g_player.score['minus'] += self.hp_points

        if self.hp_points > self.gp_points:
            self.h_player.wins += 1
        else:
            self.g_player.wins += 1

    def score(self):
        return self.hp_points, self.gp_points

    def get_history(self):
        return self._history

    def save_match_results(self, filename="results.json"):
        result = {
            "date": self._datetime.strftime("%Y-%m-%d %H:%M:%S"),
            "house_player": self.h_player.nickname,
            "guest_player": self.g_player.nickname,
            "score": self.score()
        }
        results = jsonfile_read(filename) or []
        results.append(result)
        jsonfile_write(filename, results)


def load_players(json_file: str):
    players = []
    try:
        data = jsonfile_read(json_file)
        for row in data:
            players.append(Player(row['nickname'], Gender(row['gender']), row['state']))
    except Exception as error:
        print(f'Error: {error}')
        return []
    return players
