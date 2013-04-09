from cgi import urlparse, escape
from pymongo import MongoClient
from bson.json_util import dumps, loads
import json
import ast

def application(environ, start_response):
    response_body = 'Caglar Suleyman ve Ali 3 kisiydiler'
    status = '200 OK'
    response_body = ''
    d = urlparse.parse_qsl(environ['QUERY_STRING'])

    genres = []; ratings = []; years = []; querrry = 0;
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
    if len(d)<3:
        response_body += "I DONT KNOW WHAT TO RETURN to yavuz! \n \n"

    if querrry == 1:
        try:
            connection = MongoClient("localhost", 27072)       
            db = connection.test_database
            test_collect = db.posts
            query01 = {"year":{"$gte": int(years[0]), "$lt": int(years[1])}, "rating":{"$gte": float(ratings[0]), "$lte": float(ratings[1])}, "genres":{"$in": genres}}
            result01 = test_collect.find(query01)
            response_body = dumps(result01,encoding="latin-1")
        except:
            response_body += "I DONT KNOW FROM WHERE TO RETURN to ccan! \n \n"
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

