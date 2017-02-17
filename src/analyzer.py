from src.analyzer_prepare import *
import numpy

sessions = SessionsData()
sessions.split_load_sessions("../data/split")

teams = TeamsCollector()
sessions.scan(teams)
ordered_teams = []
ordered_teams.extend(teams.teams)
ordered_teams = sorted(ordered_teams)
for i, name in enumerate(ordered_teams):
    print("{} - {}", i, name)

prepare = PrepareData()
prepare.print_verbose = False

prediction_games = []
session_round = SessionRound("2016/2017", "	מחזור 23")
game = Game(session_round, team1=ordered_teams[22], team2=ordered_teams[11],time=datetime.strptime("2017-02-18 20:29", '%Y-%m-%d %H:%M'))
prediction_games.append(game)
matrix = prepare.prepare_data_matrix(sessions,predictions_games=prediction_games)

numpy.savetxt("../data/matrix.txt", matrix, '% 8d')
