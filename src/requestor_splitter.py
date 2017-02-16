from src.requestor_model import *

db = shelve.open("../data/league_shelve.txt")
sessions1 = db["DATA"]
db.close()
print(sessions1.sessions.keys())
sessions1.split_save()
before = str(sessions1)
print(before)

sessions2 = SessionsData()
sessions2.split_load()
print(sessions2.sessions.keys())
after = str(sessions2)
print(after)

print("len1 {} len2 {} equal {}".format(len(before), len(after), before == after))
print("equal {}".format(sessions1 == sessions2))
