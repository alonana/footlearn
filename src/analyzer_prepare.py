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
        self.info("{} rows skipped, {} rows collected".format(skipped, len(data_matrix)))
        return data_matrix

    def prepare_row(self, game):
        self.verbose("analyzing game {}".format(game))
        row = {}
        for prev_index in range(1, HISTORY + 1):
            previous_session = self.sessions_collector.get_previous(game.session_round, prev_index)
            if previous_session is None:
                return None
            rank1 = self.positions_collector.get_rank(previous_session, game.team1)
            if rank1 is None:
                return None
            row["X01_PREV_RANK1_HISTORY{}".format(prev_index)] = rank1.rank
            rank2 = self.positions_collector.get_rank(previous_session, game.team2)
            if rank2 is None:
                return None
            row["X02_PREV_RANK2_HISTORY{}".format(prev_index)] = rank2.rank
            # TODO: implement me
            prev1_game = self.games_collector.get(game.team1, previous_session)
            if prev1_game is None:
                return None
            row["X03_PREV_WIN_HISTORY{}".format(prev_index)] = prev1_game

        game_result = game.get_result(game.team1)

        row["Y1_WIN"] = int(game_result == GameResult.WIN)
        # row["Y2_EVEN"] = int(game_result == GameResult.EVEN)
        # row["Y3_LOSS"] = int(game_result == GameResult.LOSS)
        self.verbose(sorted(row.items()))

        matrix_row = []
        for key in sorted(row.keys()):
            matrix_row.append(row[key])
        self.verbose(matrix_row)
        return matrix_row
