from requestor_model import *


class TeamsCollector(SessionsScanner):
    def __init__(self):
        self.teams = set()

    def game_node(self, game):
        pass

    def position_node(self, position):
        self.teams.add(position.team)


class TeamCollector(SessionsScanner):
    def __init__(self, team_name):
        self.team_name = team_name
        self.games = []

    def game_node(self, game):
        if game.team1 == self.team_name or game.team2 == self.team_name:
            self.games.append(game)

    def position_node(self, position):
        pass


class SessionsCollector(SessionsScanner):
    def __init__(self):
        self.sessions = []

    def __str__(self):
        return str(self.sessions)

    def game_node(self, game):
        self.add(game.session_round)

    def position_node(self, position):
        self.add(position.session_round)

    def add(self, session_round):
        if not session_round in self.sessions:
            self.sessions.append(session_round)

    def get_previous(self, session_round):
        index = self.sessions.index(session_round)
        if index == 0:
            return None
        return self.sessions[index - 1]


class PositionCollector(SessionsScanner):
    def __init__(self):
        self.positions = {}

    def game_node(self, game):
        pass

    @staticmethod
    def key(session_round, team):
        return "{} {}".format(session_round, team)

    def position_node(self, position):
        self.positions[self.key(position.session_round, position.team)] = position

    def get_position(self, session_round, team):
        return self.positions[self.key(session_round, team)]
