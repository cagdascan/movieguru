import pymongo
from pymongo import MongoClient

connection = MongoClient("localhost", 27072)
db = connection.mov_db01_alpha



def dbPut01(idM, title, plink, r, ur, genres, sp, d, a, date, keys):
    if len(a)>4:
        a = a[0:4]
    if len(keys)>15:
        keys = keys[0:15]

    jsonofme = {"_id": idM, "name" : title, "pLink" : plink, "rating" : r, "userRating" : ur, "genres" : genres, "plotS" : sp, "director" : d, "actors" : a, "date" : date, "keywords" : keys}

    posts = db.movies02
    posts.insert(jsonofme)
