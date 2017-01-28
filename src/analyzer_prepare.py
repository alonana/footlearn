import shelve

from src.analyzer_model import *

HISTORY = 5


class PrepareData:
    def __init__(self):
        self.print_verbose = False
        self.print_info = True
        self.sessions_collector = SessionsCollector()
        self.positions_collector = RankCollector()
        self.games_collector = GamesCollector()
        self.last_data = None

    def verbose(self, message):
        if self.print_verbose:
            print(message)

    def info(self, message):
        if self.print_info:
            print(message)

    def prepare_data_matrix(self):
        db = shelve.open("../data/league_shelve.txt")
        sessions = db["DATA"]
        db.close()

        self.verbose("collecting sessions")
        sessions.scan(self.sessions_collector)
        self.verbose(self.sessions_collector)

        self.verbose("collecting positions")
        sessions.scan(self.positions_collector)

        self.verbose("collecting games")
        sessions.scan(self.games_collector)

        data_matrix = []
        skipped = 0
        self.verbose("creating features")
        for game in self.games_collector.games:
            data_row = self.prepare_row(game)
            if data_row is None:
                self.verbose("skipping game")
                skipped += 1
            else:
                data_matrix.append(data_row)
        self.info(self.last_data)
        self.info("{} rows skipped, {} rows collected".format(skipped, len(data_matrix)))
        return data_matrix

    def prepare_row(self, game: Game):
        self.last_data = str(game) + "\n"
        self.verbose("analyzing game {}".format(game))
        row = {}
        for prev_index in range(1, HISTORY + 1):
            previous_session = self.sessions_collector.get_previous(game.session_round, prev_index)
            if previous_session is None:
                return None
            if not self.prepare_row_rank(row, previous_session, game.team1, "X01a", prev_index):
                return None
            if not self.prepare_row_rank(row, previous_session, game.team2, "X01b", prev_index):
                return None
            if not self.prepare_row_game(row, previous_session, game.team1, "X02a", prev_index):
                return None
            if not self.prepare_row_game(row, previous_session, game.team2, "X02b", prev_index):
                return None

        game_result = game.get_result(game.team1)

        row["Y1_WIN"] = int(game_result == GameResult.WIN)
        # row["Y2_EVEN"] = int(game_result == GameResult.EVEN)
        # row["Y3_LOSS"] = int(game_result == GameResult.LOSS)
        self.verbose(sorted(row.items()))

        matrix_row = []
        for key in sorted(row.keys()):
            value = row[key]
            self.last_data += "{}={}\n".format(key, value)
            matrix_row.append(value)
        self.verbose(matrix_row)
        return matrix_row

    def prepare_row_rank(self, row, session_round, team, prefix, prev_index):
        rank = self.positions_collector.get_rank(session_round, team)
        if rank is None:
            self.verbose("missing prev rank")
            return False
        row[prefix + "_PREV_RANK_HISTORY{}".format(prev_index)] = rank.rank
        return True

    def prepare_row_game(self, row, session_round, team, prefix, prev_index):
        prev_game = self.games_collector.get_by_session_and_team(session_round, team)
        if prev_game is None:
            self.verbose("missing prev game")
            return False

        game_result = prev_game.get_result(team)
        row[prefix + "_PREV_GAME_WIN_HISTORY{}".format(prev_index)] = int(game_result == GameResult.WIN)
        row[prefix + "_PREV_GAME_EVEN_HISTORY{}".format(prev_index)] = int(game_result == GameResult.EVEN)
        row[prefix + "_PREV_GAME_LOSS_HISTORY{}".format(prev_index)] = int(game_result == GameResult.LOSS)
        row[prefix + "_PREV_GAME_GOAL_SCORED_HISTORY{}".format(prev_index)] = prev_game.get_goals_scored(team)
        row[prefix + "_PREV_GAME_GOAL_SUFFERED_HISTORY{}".format(prev_index)] = prev_game.get_goals_suffered(team)

        return True
