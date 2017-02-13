import shelve
import datetime

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

        self.prepare_row_same_game(row, game, "X03")
        row["X04_DAY"] = game.time.weekday()
        row["X04_DAY_SATURDAY"] = int(game.time.weekday() == 5)
        row["X04_HOUR"] = game.time.hour
        row["X04_HOUR_LATE"] = int(game.time.hour >= 20)

        game_result = game.get_result(game.team1)

        row["Y1_WIN"] = int(game_result == GameResult.WIN)
        row["Y2_EVEN"] = int(game_result == GameResult.EVEN)
        row["Y3_LOSS"] = int(game_result == GameResult.LOSS)
        self.verbose(sorted(row.items()))

        matrix_row = []
        for key in sorted(row.keys()):
            value = row[key]
            self.last_data += "{}={}\n".format(key, value)
            matrix_row.append(value)
        self.verbose(matrix_row)
        return matrix_row

    def prepare_row_rank(self, row, session_round: SessionRound, team, prefix, prev_index):
        rank = self.positions_collector.get_rank(session_round, team)
        if rank is None:
            self.verbose("missing prev rank")
            return False
        row[prefix + "_PREV_RANK_HISTORY{}".format(prev_index)] = rank.rank
        return True

    def prepare_row_game(self, row, session_round: SessionRound, team, prefix, prev_index):
        prev_game = self.games_collector.get_by_session_and_team(session_round, team)
        if prev_game is None:
            self.verbose("missing prev game")
            return False

        game_result = prev_game.get_result(team)
        row["{}_PREV_GAME_HISTORY{}_WIN".format(prefix, prev_index)] = int(game_result == GameResult.WIN)
        row["{}_PREV_GAME_HISTORY{}_EVEN".format(prefix, prev_index)] = int(game_result == GameResult.EVEN)
        row["{}_PREV_GAME_HISTORY{}_LOSS".format(prefix, prev_index)] = int(game_result == GameResult.LOSS)
        row["{}_PREV_GAME_HISTORY{}_GOAL_SCORED".format(prefix, prev_index)] = prev_game.get_goals_scored(team)
        row["{}_PREV_GAME_HISTORY{}_GOAL_SUFFERED".format(prefix, prev_index)] = prev_game.get_goals_suffered(team)
        row["{}_PREV_GAME_HISTORY{}_DAY".format(prefix, prev_index)] = prev_game.time.weekday()
        row["{}_PREV_GAME_HISTORY{}_SATURDAY".format(prefix, prev_index)] = int(prev_game.time.weekday() == 5)
        row["{}_PREV_GAME_HISTORY{}_HOUR".format(prefix, prev_index)] = prev_game.time.hour
        row["{}_PREV_GAME_HISTORY{}_HOUR_LATE".format(prefix, prev_index)] = int(prev_game.time.hour >= 20)
        return True

    def prepare_row_same_game(self, row, game: Game, prefix):
        history_game = game
        for history in range(0, HISTORY):
            if history_game is not None:
                history_game = self.games_collector.get_prev_by_teams_before_session(history_game.session_round,
                                                                                     game.team1, game.team2)
            exists = 0
            win = -10000
            even = -10000
            loss = -10000
            scored = -10000
            suffered = -10000
            weekday = -10000
            saturday = -10000
            hour = -10000
            hour_late = -10000

            if history_game is not None:
                self.verbose("same game located: {}".format(history_game))
                game_result = history_game.get_result(game.team1)
                exists = 1
                win = int(game_result == GameResult.WIN)
                even = int(game_result == GameResult.EVEN)
                loss = int(game_result == GameResult.LOSS)
                scored = history_game.get_goals_scored(game.team1)
                suffered = history_game.get_goals_suffered(game.team1)
                weekday = history_game.time.weekday()
                saturday = int(history_game.time.weekday() == 5)
                hour = history_game.time.hour
                hour_late= int(history_game.time.hour>=20)

            row["{}_SAME_GAME_HISTORY{}".format(prefix, history)] = exists
            row["{}_SAME_GAME_HISTORY{}_WIN".format(prefix, history)] = win
            row["{}_SAME_GAME_HISTORY{}_EVEN".format(prefix, history)] = even
            row["{}_SAME_GAME_HISTORY{}_LOSS".format(prefix, history)] = loss
            row["{}_SAME_GAME_HISTORY{}_GOAL_SCORED".format(prefix, history)] = scored
            row["{}_SAME_GAME_HISTORY{}_GOAL_SUFFERED".format(prefix, history)] = suffered
            row["{}_SAME_GAME_HISTORY{}_DAY".format(prefix, history)] = weekday
            row["{}_SAME_GAME_HISTORY{}_SATURDAY".format(prefix, history)] = saturday
            row["{}_SAME_GAME_HISTORY{}_HOUR".format(prefix, history)] = hour
            row["{}_SAME_GAME_HISTORY{}_HOUR_LATE".format(prefix, history)] = hour_late
