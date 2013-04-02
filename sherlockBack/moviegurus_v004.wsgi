from cgi import urlparse, escape
from pymongo import MongoClient
from bson.json_util import dumps, loads
from bson.code import Code
from random import shuffle
import json
import ast

def application(environ, start_response):
    response_body = 'Caglar Suleyman ve Ali 3 kisiydiler'
    status = '200 OK'
    response_body = ''
    d = urlparse.parse_qsl(environ['QUERY_STRING'])

    genres = []; ratings = []; years = []; querrry = 0; keysinmov = [];
    theUser = [];
    for i in d:
        if i[0] == 'genre':
            genres.append(i[1])
        if i[0] == 'rating':
            ratings.append(i[1])
        if i[0] == 'year':
            years.append(i[1])
            if i[1] == '1800':
                years.append('1980')
            else:
                years.append(str(int(i[1])+10))
        if i[0] == 'query':
            querrry = int(i[1])
        if i[0] == 'keyword':
            keysinmov.append(i[1])
    if len(d)<1:
        response_body += "I DONT KNOW WHAT TO RETURN to yavuz! \n \n"

    if querrry == 1:
        # first query for no modification for login '''
        try:
            # first querry: dismissed prototype '''
            connection = MongoClient("localhost", 27072)       
            db = connection.test_database
            test_collect = db.posts
            query01 = {"year":{"$gte": int(years[0]), "$lt": int(years[1])}, "rating":{"$gte": float(ratings[0]), "$lte": float(ratings[1])}, "genres":{"$in": genres}}
            result01 = test_collect.find(query01)
            response_body = dumps(result01)
        except:
            response_body += "I DONT KNOW FROM WHERE TO RETURN to ccan! \n \n 1"
    elif querrry == 20:
        # second query; returns keywords for selected genres with scoring for not logged
        try:
            connection = MongoClient("localhost",27072)
            db = connection.mov_db01_alpha
            collection = db.movies02
            response_body += "q2ch1"
            result02 = collection.aggregate([{"$match":{"genres":{"$in":genres}}},{"$unwind": "$genres"},{"$match":{"genres":{"$in":genres}}},{"$group":{"_id":{"name":"$name","keys":"$keywords"}, "Gcount":{"$sum":1}}},{"$match":{"Gcount":{"$gte":len(genres)}}},{"$unwind":"$_id.keys"},{"$group":{"_id":"$_id.keys", "Kcount":{"$sum":1}}},{"$sort":{"Kcount":-1}},{"$limit":100},{"$project":{"_id":1, "value":"$Kcount"}}])
            response_body += "q2ch2"
            response_body = dumps(result02["result"])
        except:
            response_body += "nothing else matters"
    elif querrry == 30:
        # third query; returns movies for selected genres and keywords with scoring for not logged
        try:
            connection = MongoClient("localhost",27072)
            db = connection.mov_db01_alpha
            collection = db.movies02
            response_body += "1"
            result03 = collection.aggregate([{"$match":{"genres":{"$in":genres}}}, {"$unwind":"$genres"},{"$match":{"genres":{"$in":genres}}},{"$group":{"_id":{"n":"$name", "id":"$_id", "pL":"$pLink", "di":"$director", "da":"$date", "uR":"$userRating", "keys":"$keywords", "pS":"$plotS", "a":"$actors"}, "gCount":{"$sum":1}}},{"$match":{"gCount":{"$gte":len(genres)}}},{"$match":{"_id.keys":{"$in":keysinmov}}},{"$unwind":"$_id.keys"},{"$match":{"_id.keys":{"$in":keysinmov}}},{"$group":{"_id":{"name":"$_id.n", "_id":"$_id.id", "pL":"$_id.pL", "di":"$_id.di", "da":"$_id.da", "uR":"$_id.uR", "pS":"$_id.pS", "a":"$_id.a"}, "kCount":{"$sum":1}}},{"$sort":{"kCount":-1}}, {"$limit":10}, {"$project":{"_id":0, "name":"$_id.name","date":"$_id.da","pLink":"$_id.pL", "director":"$_id.di", "date":"$_id.da", "userRating":"$_id.uR", "plotS":"$_id.pS", "actors":"$_id.a"}}]) 
            response_body += "2"
            response_body += "3"
            response_body = dumps(result03["result"]) #+ "\n".join([x for x in rarray])         
        except:
            response_body += "harvester of sorrow"

     elif querrry == 21:
        # second query; returns keywords for selected genres with scoring for logged... No modifications
        try:
            connection = MongoClient("localhost",27072)
            db = connection.mov_db01_alpha
            collection = db.movies02
            response_body += "q2ch1"
            result02 = collection.aggregate([{"$match":{"genres":{"$in":genres}}},{"$unwind": "$genres"},{"$match":{"genres":{"$in":genres}}},{"$group":{"_id":{"name":"$name","keys":"$keywords"}, "Gcount":{"$sum":1}}},{"$match":{"Gcount":{"$gte":len(genres)}}},{"$unwind":"$_id.keys"},{"$group":{"_id":"$_id.keys", "Kcount":{"$sum":1}}},{"$sort":{"Kcount":-1}},{"$limit":100},{"$project":{"_id":1, "value":"$Kcount"}}])
            response_body += "q2ch2"
            response_body = dumps(result02["result"])
        except:
            response_body += "nothing else matters"
    elif querrry == 31:
        # third query; returns movies for selected genres and keywords with scoring for logged... 
        
        for i in d:
            if i[0] == "userid":
                theUserId.append(i[1])
            
        try:
            connection = MongoClient("localhost",27072)
            db = connection.mov_db01_alpha
            collection = db.movies02
            ucollection = db.users01
            theUser = ucollection.find_one({"_id":theUserId[0]})
            theUserLength = len(theUser)
            response_body += "1"
            result03 = collection.aggregate([{"$match":{"genres":{"$in":genres}}}, {"$unwind":"$genres"},{"$match":{"genres":{"$in":genres}}},{"$group":{"_id":{"n":"$name", "id":"$_id", "pL":"$pLink", "di":"$director", "da":"$date", "uR":"$userRating", "keys":"$keywords", "pS":"$plotS", "a":"$actors"}, "gCount":{"$sum":1}}},{"$match":{"gCount":{"$gte":len(genres)}}},{"$match":{"_id.keys":{"$in":keysinmov}}},{"$unwind":"$_id.keys"},{"$match":{"_id.keys":{"$in":keysinmov}}},{"$group":{"_id":{"name":"$_id.n", "_id":"$_id.id", "pL":"$_id.pL", "di":"$_id.di", "da":"$_id.da", "uR":"$_id.uR", "pS":"$_id.pS", "a":"$_id.a"}, "kCount":{"$sum":1}}},{"$match":{"_id._id":{"$nin":theUser['watchedL']}}}, {"$sort":{"kCount":-1}}, {"$limit":10}, {"$project":{"_id":0, "name":"$_id.name","date":"$_id.da","pLink":"$_id.pL", "director":"$_id.di", "date":"$_id.da", "userRating":"$_id.uR", "plotS":"$_id.pS", "actors":"$_id.a"}}]) 
            response_body += "2"
            response_body += "3"
            response_body = dumps(result03["result"])         
        except TypeError:
            response_body += "no user found"
        except:
            response_body += "harvester of sorrow"
 
    elif querrry == 'test':
        try:
            connection = MongoClient("localhost", 27072)
            db = connection.mov_db01_alpha
            collection = db.movies01
        except:
            response_body += "fafafa ReverSED"
    else:
        try:
            connection = MongoClient("localhost", 27072)       
            db = connection.test_database
            test_collect = db.posts
            query01 = {"year":{"$gte": int(years[0]), "$lt": int(years[1])}, "rating":{"$gte": float(ratings[0]), "$lte": float(ratings[1])}, "genres":{"$in": genres}}
            result01 = test_collect.find(query01)
            response_body = dumps(result01,encoding="latin-1")
        except:
            response_body += "I DONT KNOW FROM WHERE TO RETURN to ccan! \n \n"



     

    response_headers = [('Content-Type', 'text/plain'), ('Content-Length', str(len(response_body)))]

    start_response(status, response_headers)
   
#    d = urlparse.parse_qsl(environ['QUERY_STRING'])
#    temp = 'sas'
#    for i in d
#        for j in i
#            temp = temp + str(j)
    return [response_body]
#    genres = []
#    years = []
#    ratings = []

#    for i in range(len(d)):
#        if d[i][0] == 'genre':
#            genres.append(d[i][1])
#        if d[i][0] == 'year':
#            years.append(d[i][1])
#        if d[i][0] == 'rating':
#            ratings.append(d[i][1])
 
#    connection = MongoClient("localhost", 27017)
#    db = connection.test_database
#    collection = db.posts

#    if years[0] == "1800":
#        years.append("1979")
#    else:
#        years.append(str(int(years[0])+9)) 
   
#    result02 = collection.find({"year":{"$gte": int(years[0]), "$lte": int(years[1])}, "rating":{"$gte": float(ratings[0]), "$lte": float(ratings[1])}, "genres":{"$in": genres}}) 
#    resultJ = dumps(result02)

   
#    response_body = resultJ
#    response_body = years[0] + genres[0]+ ratings
#    status='200 OK'
#    output='Hello World!'

#    response_headers1 = [('Content-type', 'application/json')]#, ('Content-Length', str(len(response_body)))]
#    response_headers2 = [('Content-type', 'text/html'), ('Content-Length', str(len(response_body)))]
 
#    start_response(status, response_headers2)

#    return output #response_body

