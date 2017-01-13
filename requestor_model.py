
class SessionsData:
    def __init__(self):
        self.sessions = {}

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str(self.sessions)

    def add(self, name, session_data):
        self.sessions[name] = session_data


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


class RoundData:
    def __init__(self):
        self.positions = []
        self.games = []

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "{{games: {}, positions: {}}}".format(self.games, self.positions)

    def add_position(self, table):
        self.positions.append(table)

    def add_game(self, table):
        self.games.append(table)

