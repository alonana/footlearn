import numpy

from src.analyzer_prepare import *

sessions = SessionsData()
sessions.split_load_sessions("../data/split")

teams = TeamsCollector()
sessions.scan(teams)
ordered_teams = []
ordered_teams.extend(teams.teams)
ordered_teams = sorted(ordered_teams)
for i, name in enumerate(ordered_teams):
    print("{} - {}".format(i, name))

prediction_games = []
session_round = SessionRound(2017, 23)
prediction_games.append(Game(session_round, team1=ordered_teams[22], team2=ordered_teams[11],
                             time=datetime.strptime("2017-02-18 20:29", '%Y-%m-%d %H:%M')))
prediction_games.append(Game(session_round, team1=ordered_teams[4], team2=ordered_teams[21],
                             time=datetime.strptime("2017-02-19 18:29", '%Y-%m-%d %H:%M')))
prediction_games.append(Game(session_round, team1=ordered_teams[6], team2=ordered_teams[5],
                             time=datetime.strptime("2017-02-19 20:14", '%Y-%m-%d %H:%M')))
prediction_games.append(Game(session_round, team1=ordered_teams[15], team2=ordered_teams[0],
                             time=datetime.strptime("2017-02-20 20:59", '%Y-%m-%d %H:%M')))

prepare = PrepareData()
matrix = prepare.prepare_data_matrix(sessions, predictions_games=prediction_games, prepare_data=False)
numpy.savetxt("../data/matrix_predictions.txt", matrix, '% 8d')
