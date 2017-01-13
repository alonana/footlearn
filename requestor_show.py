import shelve

from requestor_model import RoundData
from requestor_model import SessionData
from requestor_model import SessionsData

SessionsData()
SessionData()
RoundData()

db = shelve.open("league_shelve.txt")
data = db["DATA"]
print(data)

db.close()
