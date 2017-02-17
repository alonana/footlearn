from abc import ABCMeta, abstractmethod
from datetime import datetime
from enum import Enum
import shelve
import re
import os


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

    def __lt__(self, other):
        if self.session_name == other.session_name:
            return self.round_number < other.round_number
        return self.session_name < other.session_name

    def __le__(self, other):
        if self.session_name == other.session_name:
            return self.round_number <= other.round_number
        return self.session_name <= other.session_name

    def __ge__(self, other):
        if self.session_name == other.session_name:
            return self.round_number >= other.round_number
        return self.session_name >= other.session_name


class Game:
    def __init__(self, session_round, data_dictionary=None, team1=None, team2=None, time=None):
        self.session_round = session_round
        if data_dictionary is None:
            self.team1 = team1
            self.team2 = team2
            self.time = time
            self.goals1 = -1
            self.goals2 = -1
            self.court = "NA"
        else:
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
    def get_result_by_score(score1, score2) -> GameResult:
        if score1 > score2:
            return GameResult.WIN
        if score1 < score2:
            return GameResult.LOSS
        return GameResult.EVEN

    def get_result(self, team) -> GameResult:
        if team == self.team1:
            return self.get_result_by_score(self.goals1, self.goals2)
        if team == self.team2:
            return self.get_result_by_score(self.goals2, self.goals1)
        raise Exception('team {} is not in game {}'.format(team, self))

    def get_goals_scored(self, team) -> int:
        if team == self.team1:
            return self.goals1
        if team == self.team2:
            return self.goals2
        raise Exception('team {} is not in game {}'.format(team, self))

    def get_goals_suffered(self, team) -> int:
        if team == self.team1:
            return self.goals2
        if team == self.team2:
            return self.goals1
        raise Exception('team {} is not in game {}'.format(team, self))

    def includes_teams(self, team1, team2) -> bool:
        return (self.team1 == team1 and self.team2 == team2) or (self.team1 == team2 and self.team2 == team1)


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


class SessionsScanner(metaclass=ABCMeta):
    @abstractmethod
    def scan_game_node(self, game: Game):
        pass

    @abstractmethod
    def scan_rank_node(self, rank: Position):
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

    def __eq__(self, other):
        return self.sessions == other.sessions

    def add(self, name, session_data):
        self.sessions[name] = session_data

    def scan(self, scanner):
        for session_name in sorted(self.sessions.keys()):
            session_data = self.sessions[session_name]
            session_data.scan(scanner, session_name.split('/')[1])

    def print(self):
        scanner = PrintScanner()
        self.scan(scanner)

    def split_save_sessions(self, root_folder):
        for name, data in self.sessions.items():
            safe_name = re.sub('[^0-9a-zA-Z]+', '_', name)
            folder = "{}/{}".format(root_folder, safe_name)
            os.makedirs(folder)
            session_file_name = "{}/session_name.txt".format(folder)
            with open(session_file_name, "w") as session_file:
                session_file.write(name)
            session_data_folder = "{}/data".format(folder)
            os.makedirs(session_data_folder)
            data.split_save_session(session_data_folder)

    def split_load_sessions(self, root_folder):
        for folder_name in os.listdir(root_folder):
            folder = "{}/{}".format(root_folder, folder_name)
            session_file_name = "{}/session_name.txt".format(folder)
            with open(session_file_name, "r") as session_file:
                name = session_file.read()
            data = SessionData()
            session_data_folder = "{}/data".format(folder)
            data.split_load_session(session_data_folder)
            self.sessions[name] = data


class SessionData:
    def __init__(self):
        self.rounds = {}

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str(self.rounds)

    def __eq__(self, other):
        return self.rounds == other.rounds

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

    def split_save_session(self, folder_path):
        for name, data in self.rounds.items():
            splitted = SessionData()
            splitted.rounds[name] = data
            name_safe = re.sub('[^0-9a-zA-Z]+', '_', name)
            db = shelve.open("{}/{}.txt".format(folder_path, name_safe))
            db["DATA"] = splitted
            db.close()

    def split_load_session(self, folder_path):
        for file_name in os.listdir(folder_path):
            file_path = "{}/{}".format(folder_path, file_name)
            db = shelve.open(file_path)
            print("loading {}".format(file_path))
            splitted = db["DATA"]
            db.close()
            self.rounds.update(splitted.rounds)


class RoundData:
    def __init__(self):
        self.positions = []
        self.games = []

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "{{\n\tgames: {},\n\tpositions: {}}}".format(self.games, self.positions)

    def __eq__(self, other):
        return self.positions == other.positions and self.games == other.games

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
