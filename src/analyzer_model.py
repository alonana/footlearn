from src.requestor_model import *


class TeamsCollector(SessionsScanner):
    def __init__(self):
        self.teams = set()

    def scan_game_node(self, game: Game):
        pass

    def scan_rank_node(self, rank: Position):
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

    def get_previous(self, session_round: SessionRound, steps):
        index = self.sessions.index(session_round)
        index -= steps
        if index < 0:
            return None
        return self.sessions[index]

    def add_if_required(self, session_round):
        if not session_round in self.sessions:
            self.sessions.append(session_round)
            self.sessions = sorted(self.sessions)


class GamesCollector(SessionsScanner):
    def __init__(self):
        self.games = []
        self.games_by_session_and_team = {}

    def __str__(self):
        return str(self.games)

    def scan_game_node(self, game):
        self.games.append(game)
        self.games_by_session_and_team[self.get_key(game.session_round, game.team1)] = game
        self.games_by_session_and_team[self.get_key(game.session_round, game.team2)] = game

    def scan_rank_node(self, rank):
        pass

    @staticmethod
    def get_key(session_round, team):
        return "{} {}".format(session_round, team)

    def get_by_session_and_team(self, session_round: SessionRound, team: str) -> Game:
        key = self.get_key(session_round, team)
        if key in self.games_by_session_and_team:
            return self.games_by_session_and_team[key]
        return None

    def get_prev_by_teams_before_session(self, session_round: SessionRound, team1, team2) -> Game:
        for game in reversed(self.games):
            if game.session_round >= session_round:
                continue
            if not game.includes_teams(team1, team2):
                continue
            return game
        return None


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

    def get_rank(self, session_round: SessionRound, team):
        key = self.key(session_round, team)
        if key in self.ranks.keys():
            return self.ranks[key]
        return None
