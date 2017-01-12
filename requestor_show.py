import shelve
import json

db = shelve.open("league_shelve.txt")
data = db["DATA"]
print(json.dumps(data,indent=3, ensure_ascii=False))

db.close()