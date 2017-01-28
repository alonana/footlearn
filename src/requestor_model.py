from abc import ABCMeta, abstractmethod
from datetime import datetime
from enum import Enum


class SessionsScanner(metaclass=ABCMeta):
    @abstractmethod
    def scan_game_node(self, game):
        pass

    @abstractmethod
    def scan_rank_node(self, rank):
        pass


class PrintScanner(SessionsScanner):
    def scan_game_node(self, game):
        print(game)

    def scan_rank_node(self, rank):
        print(rank)


class SessionsData:
    def __init__(self):
        self.sessions = {}

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str(self.sessions)

    def add(self, name, session_data):
        self.sessions[name] = session_data

    def scan(self, scanner):
        for session_name in sorted(self.sessions.keys()):
            session_data = self.sessions[session_name]
            session_data.scan(scanner, session_name.split('/')[1])

    def print(self):
        scanner = PrintScanner()
        self.scan(scanner)


class SessionData:
    def __init__(self):
        self.rounds = {}

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str(self.rounds)

    def add_position(self, round_name, table):
        round_data = self.get_round_data(round_name)
        round_data.add_position(table)

    def add_game(self, round_name, table):
        round_data = self.get_round_data(round_name)
        round_data.add_game(table)

    def get_round_data(self, round_name):
        if round_name in self.rounds.keys():
            round_data = self.rounds[round_name]
        else:
            round_data = RoundData()
            self.rounds[round_name] = round_data
        return round_data

    def scan(self, scanner, session_name):
        round_name_prefix = 'מחזור '
        round_numbers = []
        for round_name in self.rounds.keys():
            cut_name = round_name[len(round_name_prefix):]
            if cut_name.isdigit():
                round_numbers.append(int(cut_name))
        for round_number in sorted(round_numbers):
            round_name = "{}{}".format(round_name_prefix, round_number)
            round_data = self.rounds[round_name]
            round_data.scan(scanner, session_name, round_number)


class RoundData:
    def __init__(self):
        self.positions = []
        self.games = []

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "{{\n\tgames: {},\n\tpositions: {}}}".format(self.games, self.positions)

    def add_position(self, table):
        self.positions.append(table)

    def add_game(self, table):
        self.games.append(table)

    def scan(self, scanner, session_name, round_number):
        session_round = SessionRound(session_name, round_number)
        for round_games in self.games:
            for game in round_games:
                scanner.scan_game_node(Game(session_round, game))
        for round_position in self.positions:
            for position in round_position:
                scanner.scan_rank_node(Position(session_round, position))


class GameResult(Enum):
    WIN = 1,
    EVEN = 2,
    LOSS = 3

    def __eq__(self, other):
        return self.value == other.value

    def __ne__(self, other):
        return self.value != other.value


class SessionRound:
    def __init__(self, session_name, round_number):
        self.session_name = session_name
        self.round_number = round_number

    def __str__(self):
        return "{} {}".format(self.session_name, self.round_number)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.round_number == other.round_number and self.session_name == other.session_name


class Game:
    def __init__(self, session_round, data_dictionary):
        self.session_round = session_round
        players = data_dictionary['משחק'].split('-')
        self.team1 = players[0].strip()
        self.team2 = players[1].strip()
        goals = data_dictionary['תוצאה'].split('-')
        self.goals1 = int(goals[1].strip())
        self.goals2 = int(goals[0].strip())
        self.time = datetime.strptime(data_dictionary['תאריך'] + " " + data_dictionary['שעה'], '%d/%m/%y %H:%M')
        self.court = data_dictionary['מגרש']

    def __str__(self):
        return "{session_round}\tgame: {team1} {goals1} vs. {team2} {goals2} at {time} located {court}". \
            format(session_round=self.session_round,
                   team1=self.team1,
                   team2=self.team2,
                   goals1=self.goals1,
                   goals2=self.goals2,
                   time=datetime.strftime(self.time, '%Y-%m-%d %H:%M'),
                   court=self.court)

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def get_result_by_score(score1, score2):
        if score1 > score2:
            return GameResult.WIN
        if score1 < score2:
            return GameResult.LOSS
        return GameResult.EVEN

    def get_result(self, team):
        if team == self.team1:
            return self.get_result_by_score(self.goals1, self.goals2)
        if team == self.team2:
            return self.get_result_by_score(self.goals2, self.goals1)
        raise Exception('team {} is not in game {}'.format(team, self))

    def get_goals_scored(self, team):
        if team == self.team1:
            return self.goals1
        if team == self.team2:
            return self.goals2
        raise Exception('team {} is not in game {}'.format(team, self))

    def get_goals_suffered(self, team):
        if team == self.team1:
            return self.goals2
        if team == self.team2:
            return self.goals1
        raise Exception('team {} is not in game {}'.format(team, self))


class Position:
    def __init__(self, session_round, data_dictionary):
        self.session_round = session_round
        self.games = data_dictionary["מש'"]
        self.loss = data_dictionary["הפ'"]
        self.rank = int(data_dictionary['מיקום'])
        self.score = data_dictionary["נק'"]
        self.team = data_dictionary['קבוצה']

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "{session_round}\tposition: {team} {rank}". \
            format(session_round=self.session_round, team=self.team, rank=self.rank)
