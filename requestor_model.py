from abc import ABCMeta, abstractmethod

class SessionsScanner(metaclass=ABCMeta):
    @abstractmethod
    def game_node(self, session_name, round_number, game):
        pass

    @abstractmethod
    def position_node(self, session_name, round_number, position):
        pass


class PrintScanner(SessionsScanner):
    def game_node(self, session_name, round_number, game):
        print("{}\t{}\t{} game: ".format(session_name, round_number, game))

    def position_node(self, session_name, round_number, position):
        print("{}\t{}\t{} position: ".format(session_name, round_number, position))


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
            session_data.scan(scanner, session_name)

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
        for round_games in self.games:
            for game in round_games:
                scanner.game_node(session_name, round_number, game)
        for round_position in self.positions:
            for position in round_position:
                scanner.position_node(session_name, round_number, position)
