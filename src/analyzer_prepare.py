import shelve

from src.analyzer_model import *


class PrepareData:
    def __init__(self):
        self.print_verbose = False
        self.print_info = True
        self.sessions_collector = SessionsCollector()
        self.positions_collector = RankCollector()

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
        games_collector = GamesCollector()
        sessions.scan(games_collector)

        data_matrix = []
        skipped = 0
        self.verbose("creating features")
        for game in games_collector.games:
            data_row = self.prepare_game(game)
            if data_row is None:
                self.verbose("skipping game")
                skipped += 1
            else:
                data_matrix.append(data_row)
        self.info("{} rows skipped, {} rows collected".format(skipped, len(data_matrix)))
        return data_matrix

    def prepare_game(self, game):
        previous_session = self.sessions_collector.get_previous(game.session_round)
        previous_rank1 = None
        previous_rank2 = None
        if previous_session is not None:
            previous_rank1 = self.positions_collector.get_rank(previous_session, game.team1)
            previous_rank2 = self.positions_collector.get_rank(previous_session, game.team2)
        game_result = game.get_result(game.team1)

        self.verbose("{:<100} result {:<20} prev1 {:<40} prev2 {:<40}".format(
            str(game),
            game_result,
            str(previous_rank1),
            str(previous_rank2)
        ))

        if previous_rank1 is None or previous_rank2 is None:
            return None
        feature1_rank1 = previous_rank1.rank
        feature2_rank2 = previous_rank2.rank
        y1_win = 0
        y2_even = 0
        y3_loss = 0
        if game_result == GameResult.WIN:
            y1_win = 1
        elif game_result == GameResult.EVEN:
            y2_even = 1
        else:
            y3_loss = 1

        self.verbose("{} {} {} {} {}".format(
            feature1_rank1,
            feature2_rank2,
            y1_win,
            y2_even,
            y3_loss
        ))
        data_row = [feature1_rank1, feature2_rank2, y1_win, y2_even, y3_loss]
        return data_row
