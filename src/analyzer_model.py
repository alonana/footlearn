from src.requestor_model import *


class TeamsCollector(SessionsScanner):
    def __init__(self):
        self.teams = set()

    def scan_game_node(self, game):
        pass

    def scan_rank_node(self, rank):
        self.teams.add(rank.team)


class TeamCollector(SessionsScanner):
    def __init__(self, team_name):
        self.team_name = team_name
        self.games = []

    def scan_game_node(self, game):
        if game.team1 == self.team_name or game.team2 == self.team_name:
            self.games.append(game)

    def scan_rank_node(self, rank):
        pass


class SessionsCollector(SessionsScanner):
    def __init__(self):
        self.sessions = []

    def __str__(self):
        return str(self.sessions)

    def scan_game_node(self, game):
        self.add(game.session_round)

    def scan_rank_node(self, rank):
        self.add(rank.session_round)

    def add(self, session_round):
        if not session_round in self.sessions:
            self.sessions.append(session_round)

    def get_previous(self, session_round):
        index = self.sessions.index(session_round)
        if index == 0:
            return None
        return self.sessions[index - 1]


class GamesCollector(SessionsScanner):
    def __init__(self):
        self.games = []

    def __str__(self):
        return str(self.games)

    def scan_game_node(self, game):
        self.games.append(game)

    def scan_rank_node(self, rank):
        pass


class RankCollector(SessionsScanner):
    def __init__(self):
        self.ranks = {}

    def scan_game_node(self, game):
        pass

    @staticmethod
    def key(session_round, team):
        return "{} {}".format(session_round, team)

    def scan_rank_node(self, rank):
        self.ranks[self.key(rank.session_round, rank.team)] = rank

    def get_rank(self, session_round, team):
        key = self.key(session_round, team)
        if key in self.ranks.keys():
            return self.ranks[key]
        return None
