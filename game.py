import datetime
from enum import Enum
from random import randrange
from files import jsonfile_read, jsonfile_write


class Gender(Enum):
    """Výčtový typ pro pohlaví"""
    male = 'man'
    female = 'woman'


class Dice:
    """Třída simulující hod kostkou s nastavitelným rozsahem hodnot."""

    @staticmethod
    def roll(max_value=6):
        """Provede hod kostkou.

        Args:
            max_value (int): Maximální hodnota (výchozí: 6, musí být 4-9).

        Returns:
            int: Náhodné číslo v rozmezí 1 až max_value (včetně).

        Raises:
            ValueError: Pokud max_value není v rozmezí 4-9.
        """
        if max_value < 4 or max_value > 9:
            raise ValueError("Maximální hodnota musí být v rozmezí 4 až 9.")
        return randrange(1, max_value + 1)


class Person:
    """Třída reprezentující osobu s přezdívkou, pohlavím a datem narození."""

    def __init__(self, nickname: str, gender: Gender):
        """Inicializuje osobu.

        Args:
            nickname (str): Přezdívka osoby.
            gender (Gender): Pohlaví osoby (instance třídy Gender).
        """
        self.nickname = nickname
        self.gender = gender
        self._birth = datetime.datetime.now()

    def __str__(self):
        """Vrací textovou reprezentaci osoby."""
        return f'Nickname: {self.nickname}, gender: {self.gender.value}'

    @property
    def gender(self):
        """Vrací pohlaví osoby."""
        return self._gender

    @gender.setter
    def gender(self, gender):
        """Nastaví pohlaví osoby.

        Args:
            gender (Gender): Pohlaví osoby.

        Raises:
            ValueError: Pokud gender není instance třídy Gender.
        """
        if isinstance(gender, Gender):
            self._gender = gender
        else:
            raise ValueError("Gender value not valid")

    def get_seconds_from_birth(self):
        """Vrací počet sekund od vzniku instance."""
        return int((datetime.datetime.now() - self._birth).total_seconds())


class Player(Person):
    """Třída reprezentující hráče s informacemi o stavů, hrách, výhrách a skóre."""

    def __init__(self, nickname: str, gender: Gender, state: str):
        """Inicializuje hráče.

        Args:
            nickname (str): Přezdívka hráče.
            gender (Gender): Pohlaví hráče (instance třídy Gender).
            state (str): Stav hráče.
        """
        super().__init__(nickname, gender)
        self.state = state
        self.count_of_games = 0
        self.wins = 0
        self.score = {'plus': 0, 'minus': 0}

    def __str__(self):
        """Vrací textovou reprezentaci hráče."""
        return f'{super().__str__()}, state: {self.state}'

    @property
    def wins(self):
        """Vrací počet výher hráče."""
        return self._wins

    @wins.setter
    def wins(self, value):
        """Nastaví počet výher hráče.

        Args:
            value (int): Počet výher.

        Raises:
            ValueError: Pokud value je záporné číslo.
        """
        if value < 0:
            raise ValueError("Property wins must not be a negative value")
        self._wins = value

    def win_rate(self):
        """Vrací procento výher hráče.

        Returns:
            float: Procento výher zaokrouhlené na 2 desetinná místa.
        """
        return round(self.wins / self.count_of_games * 100, 2) if self.count_of_games > 0 else 0.0

    def overall_score(self):
        """Vrací celkové skóre hráče.

        Returns:
            tuple: Tuple (plus_body, minus_body).
        """
        return self.score["plus"], self.score["minus"]


class Match:
    """Třída reprezentující zápas mezi dvěma hráči s logikou hry a ukládáním výsledků."""

    def __init__(self, house_player: Player, guest_player: Player, winning_score=10, max_dice_value=6):
        """Inicializuje zápas.

        Args:
            house_player (Player): Domácí hráč.
            guest_player (Player): Hostující hráč.
            winning_score (int): Počet bodů k vítězství (výchozí: 10).
            max_dice_value (int): Maximální hodnota kostky (výchozí: 6).
        """
        self.h_player = house_player
        self.g_player = guest_player
        self.winning_score = winning_score
        self.max_dice_value = max_dice_value
        self._datetime = datetime.datetime.now()
        self.hp_points = 0
        self.gp_points = 0
        self._history = []

    def __str__(self):
        """Vrací textovou reprezentaci zápasu."""
        return f'{self.h_player.nickname} vs. {self.g_player.nickname} {self.score()}'

    @property
    def h_player(self):
        """Vrací domácího hráče."""
        return self._hplayer

    @h_player.setter
    def h_player(self, player):
        """Nastaví domácího hráče.

        Args:
            player (Player): Domácí hráč.

        Raises:
            TypeError: Pokud player není instance třídy Player.
        """
        if isinstance(player, Player):
            self._hplayer = player
        else:
            raise TypeError("h_player must be instance of Player")

    @property
    def g_player(self):
        """Vrací hostujícího hráče."""
        return self._gplayer

    @g_player.setter
    def g_player(self, player):
        """Nastaví hostujícího hráče.

        Args:
            player (Player): Hostující hráč.

        Raises:
            TypeError: Pokud player není instance třídy Player.
        """
        if isinstance(player, Player):
            self._gplayer = player
        else:
            raise TypeError("g_player must be instance of Player")

    def __roll(self):
        """Provede hod kostkou pro oba hráče.

        Zajistí, aby oba hráči nehodili stejnou hodnotu (bez remízy).

        Returns:
            int: 0 pokud domácí hráč vyhraje, 1 pokud hostující hráč vyhraje.
        """
        while True:
            hp = Dice.roll(self.max_dice_value)
            gp = Dice.roll(self.max_dice_value)
            if hp != gp:
                break
        return 0 if hp > gp else 1

    def play(self):
        """Odehraje zápas mezi dvěma hráči až do dosažení výherního skóre."""
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
        """Vrací aktuální skóre zápasu.

        Returns:
            tuple: Tuple (domácí_body, hostující_body).
        """
        return self.hp_points, self.gp_points

    def get_history(self):
        """Vrací historii všech kol zápasu.

        Returns:
            list: Seznam skóre po každém kole.
        """
        return self._history

    def save_match_results(self, filename="results.json"):
        """Uloží výsledky zápasu do JSON souboru.

        Args:
            filename (str): Název souboru pro uložení (výchozí: results.json).

        Raises:
            FileNotFoundError: Pokud není cesta k souboru platná.
            IOError: Pokud došlo k chybě při čtení nebo zápisu.
        """
        try:
            result = {
                "date": self._datetime.strftime("%Y-%m-%d %H:%M:%S"),
                "house_player": self.h_player.nickname,
                "guest_player": self.g_player.nickname,
                "score": self.score()
            }
            try:
                results = jsonfile_read(filename)
            except FileNotFoundError:
                results = []
            
            results.append(result)
            jsonfile_write(filename, results)
        except (FileNotFoundError, IOError) as e:
            raise IOError(f"Chyba při ukládání výsledků zápasu: {e}")


def load_players(json_file: str):
    """Načte hráče ze JSON souboru a vytvoří seznam instancí Player.

    Args:
        json_file (str): Cesta k JSON souboru s daty o hráčích.

    Returns:
        list: Seznam instancí třídy Player.

    Raises:
        FileNotFoundError: Pokud soubor neexistuje.
        json.JSONDecodeError: Pokud soubor není validní JSON.
        KeyError: Pokud chybí povinné klíče v datech hráčů.
        ValueError: Pokud je pohlaví hráče neplatné.
    """
    players = []
    data = jsonfile_read(json_file)
    
    if not isinstance(data, list):
        raise ValueError("JSON soubor musí obsahovat seznam hráčů.")
    
    required_keys = {'nickname', 'gender', 'state'}
    
    for i, row in enumerate(data):
        if not isinstance(row, dict):
            raise ValueError(f"Řádek {i} není slovník.")
        
        missing_keys = required_keys - set(row.keys())
        if missing_keys:
            raise KeyError(f"Řádek {i} postrádá povinné klíče: {missing_keys}")
        
        try:
            gender = Gender(row['gender'])
        except ValueError:
            raise ValueError(f"Řádek {i}: Neplatné pohlaví '{row['gender']}'.")
        
        players.append(Player(row['nickname'], gender, row['state']))
    
    return players
