from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db     = client.music

def getList():
    global db
    l = []
    songs = db.song.find({})
    for item in songs:
        item.pop("_id",None)
        l.append(item)
    return l

def insert( song ):
    global db
    db.song.insert(song)

def find( data ):
    global db
    return db.song.find_one(data)
