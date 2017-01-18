import shelve

from analyzer_model import *

db = shelve.open("league_shelve.txt")
sessions = db["DATA"]
db.close()

sessions.print()

print("teams are:")
teams_collector = TeamsCollector()
sessions.scan(teams_collector)
sorted_teams = sorted(teams_collector.teams)
print("\n".join(sorted_teams))

print("sessions are:")
sessions_collector = SessionsCollector()
sessions.scan(sessions_collector)
print(sessions_collector)

print("collecting positions")
positions_collector = PositionCollector()
sessions.scan(positions_collector)

team = sorted_teams[0]
print("analyzing team {}".format(team))
group_collector = TeamCollector(team)
sessions.scan(group_collector)
for game in group_collector.games:
    prev = sessions_collector.get_previous(game.session_round)
    if prev is None:
        position = None
    else:
        position = positions_collector.get_position(prev, team)
    print("{} result {} prev position {}".format(game, game.get_result(team), position))
