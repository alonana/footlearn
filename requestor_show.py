import shelve

from requestor_model import *


class GroupsCollector(SessionsScanner):
    def __init__(self):
        self.groups = set()

    def game_node(self, session_name, round_number, game):
        pass

    def position_node(self, session_name, round_number, position):
        self.groups.add(position['קבוצה'])


# show pycharm that we need the imports
SessionsData()
SessionData()
RoundData()

db = shelve.open("league_shelve.txt")
sessions = db["DATA"]
db.close()

sessions.print()
groups_collector = GroupsCollector()
sessions.scan(groups_collector)
print("groups are:")
print("\n".join(groups_collector.groups))
group = next(iter(groups_collector.groups))
print("analyzing group {}".format(group))
