import shelve

KEY = "dict"
db = shelve.open("db.txt")
if KEY in db.keys():
    print("loading")
    dict = db[KEY]
else:
    print("creating")
    dict = {}
    dict["a"] = 1
    dict["b"] = 2
    dict["b"] = 3

    db[KEY] = dict

db.close()
print(dict)