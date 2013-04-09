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

    genres = []
    querrry = 0 
    keysinmov = []
    theUserId = ''
    ttid = ''
    ttids = []

    d = urlparse.parse_qsl(environ['QUERY_STRING'])
    for i in d:
        if i[0] == 'genre':
            genres.append(i[1])
        if i[0] == 'query':
            querrry = int(i[1])
        if i[0] == 'keyword':
            keysinmov.append(i[1]) 
        if i[0] == 'userid':
            theUserId = i[1]
        if i[0] == 'ttid':
            ttid = i[1]
        if i[0] == 'ttids':
            ttids.append(i[1])

    connection = MongoClient("localhost",27072)
    db = connection.mov_db01_alpha
    collection = db.movies02
    ucollection = db.users


    if querrry == 10:
        try:
            ucollection.insert({"_id":theUserId, "watchL":[], "watchedL":[]})
        except:
            response_body = "kullanici ekleyemedim"
         

    if querrry == 20:
        # second query; returns keywords for selected genres with scoring for not logged
        try:
            response_body += "q2ch1"
            result02 = collection.aggregate([{"$match":{"genres":{"$in":genres}}},{"$unwind": "$genres"},{"$match":{"genres":{"$in":genres}}},{"$group":{"_id":{"name":"$name","keys":"$keywords"}, "Gcount":{"$sum":1}}},{"$match":{"Gcount":{"$gte":len(genres)}}},{"$unwind":"$_id.keys"},{"$group":{"_id":"$_id.keys", "Kcount":{"$sum":1}}},{"$sort":{"Kcount":-1}},{"$limit":100},{"$project":{"_id":1, "value":"$Kcount"}}])
            response_body += "q2ch2"
            response_body = dumps(result02["result"])
        except:
            response_body += "nothing else matters"

    elif querrry == 30:
        # third query; returns movies for selected genres and keywords with scoring for not logged
        try:
            response_body += "1"
            result03 = collection.aggregate([{"$match":{"genres":{"$in":genres}}}, {"$unwind":"$genres"},{"$match":{"genres":{"$in":genres}}},{"$group":{"_id":{"n":"$name", "id":"$_id", "pL":"$pLink", "di":"$director", "da":"$date", "uR":"$userRating", "keys":"$keywords", "pS":"$plotS", "a":"$actors"}, "gCount":{"$sum":1}}},{"$match":{"gCount":{"$gte":len(genres)}}},{"$match":{"_id.keys":{"$in":keysinmov}}},{"$unwind":"$_id.keys"},{"$match":{"_id.keys":{"$in":keysinmov}}},{"$group":{"_id":{"name":"$_id.n", "_id":"$_id.id", "pL":"$_id.pL", "di":"$_id.di", "da":"$_id.da", "uR":"$_id.uR", "pS":"$_id.pS", "a":"$_id.a"}, "kCount":{"$sum":1}}},{"$sort":{"kCount":-1}}, {"$limit":10}, {"$project":{"_id":0, "ttid":"$_id._id", "name":"$_id.name","date":"$_id.da","pLink":"$_id.pL", "director":"$_id.di", "date":"$_id.da", "userRating":"$_id.uR", "plotS":"$_id.pS", "actors":"$_id.a"}}]) 
            response_body = dumps(result03["result"])       
        except:
            response_body += "harvester of sorrow"

    elif querrry == 21:
        # second query; returns keywords for selected genres with scoring for logged... No modifications
        try:
            response_body += "q2ch1"
            result02 = collection.aggregate([{"$match":{"genres":{"$in":genres}}},{"$unwind": "$genres"},{"$match":{"genres":{"$in":genres}}},{"$group":{"_id":{"name":"$name","keys":"$keywords"}, "Gcount":{"$sum":1}}},{"$match":{"Gcount":{"$gte":len(genres)}}},{"$unwind":"$_id.keys"},{"$group":{"_id":"$_id.keys", "Kcount":{"$sum":1}}},{"$sort":{"Kcount":-1}},{"$limit":100},{"$project":{"_id":1, "value":"$Kcount"}}])
            response_body += "q2ch2"
            response_body = dumps(result02["result"])
        except:
            response_body += "nothing else matters"


    elif querrry == 31:
        # third query; returns movies for selected genres and keywords with scoring for logged... watched list of the user EXCLUDED
        try:
            theUser = ucollection.find_one({"_id":theUserId})
            theUserLength = len(theUser)
            response_body += theUserId[0]#['_id']#theUserLength
            result03 = collection.aggregate([{"$match":{"genres":{"$in":genres}}}, {"$unwind":"$genres"},{"$match":{"genres":{"$in":genres}}},{"$group":{"_id":{"n":"$name", "id":"$_id", "pL":"$pLink", "di":"$director", "da":"$date", "uR":"$userRating", "keys":"$keywords", "pS":"$plotS", "a":"$actors"}, "gCount":{"$sum":1}}},{"$match":{"gCount":{"$gte":len(genres)}}},{"$match":{"_id.keys":{"$in":keysinmov}}},{"$unwind":"$_id.keys"},{"$match":{"_id.keys":{"$in":keysinmov}}},{"$group":{"_id":{"name":"$_id.n", "_id":"$_id.id", "pL":"$_id.pL", "di":"$_id.di", "da":"$_id.da", "uR":"$_id.uR", "pS":"$_id.pS", "a":"$_id.a"}, "kCount":{"$sum":1}}},{"$match":{"_id._id":{"$nin":theUser['watchedL']}}}, {"$sort":{"kCount":-1}}, {"$limit":10}, {"$project":{"_id":0, "ttid":"$_id._id", "name":"$_id.name","date":"$_id.da","pLink":"$_id.pL", "director":"$_id.di", "date":"$_id.da", "userRating":"$_id.uR", "plotS":"$_id.pS", "actors":"$_id.a"}}]) 
            response_body += "2"
            response_body += "3"
            response_body = dumps(result03["result"])         
        except TypeError:
            response_body += "no user found"
        except:
            response_body += "harvester of sorrow"


    elif querrry == 41:
        ''' inputs, ttid, userid. output, ttid added to watchList'''
        try:
            theUser = ucollection.find_one({"_id":theUserId})
            theUserLength = len(theUser)
            result41 = ucollection.update({"_id":theUserId, "watchL":{"$nin":[ttid]}},{"$push":{"watchL":ttid}}) 
        except TypeError:
            response_body = "no user found"
        except:
            response_body = "watchliste eklenemedi"

    elif querrry == 42:
        ''' inputs, userid, ttids&ttids&ttids '''
        try:
            theUser = ucollection.find_one({"_id":theUserId})
            theUserLength = len(theUser)
            result42 = ucollection.update({"_id":theUserId, "watchL":{"$nin":ttids}},{"$pushAll":{"watchL":ttids}}) 
        except TypeError:
            response_body = "no user found"
        except:
            response_body = "watchliste eklenemedi"


    elif querrry == 51:
        ''' watchedList'e ekleme. input: [userid,ttid] output: userid watchedList.append(ttid) '''
        try:
            res51 = ucollection.update({"_id":theUserId, "watchedL":{"$nin":[ttid]}},{"$push":{"watchedL":ttid}})
        except:
            response_body = "watchedliste eklenemedi"

    elif querrry == 52:
        ''' inputs, userid, ttids&ttids&ttids '''
        try:
            theUser = ucollection.find_one({"_id":theUserId})
            theUserLength = len(theUser)
            result42 = ucollection.update({"_id":theUserId, "watchedL":{"$nin":ttids}},{"$pushAll":{"watchedL":ttids}}) 
        except TypeError:
            response_body = "no user found"
        except:
            response_body = "watchliste eklenemedi"



    elif querrry == 61:
        '''q61, watchlist gosterme. input(userid) output: JSON([title,poster,ttid,userRating])'''
        try:
            res611 = ucollection.find_one({"_id":theUserId})
            wL = res611['watchL']
            res612 = collection.find({"_id":{"$in":wL}},{"_id":1,"name":1,"pLink":1, "userRating":1})
            response_body = dumps(res612)   
        except:
            response_body = "watchlisti dokemedim"

    elif querrry == 71:
        '''q71, watchedlist gosterme. input(userid) output: JSON([title,poster,ttid,userRating])'''
        try:
            res711 = ucollection.find_one({"_id":theUserId})
            wedL = res711['watchedL']
            res712 = collection.find({"_id":{"$in":wedL}},{"_id":1,"name":1,"pLink":1, "userRating":1})
            response_body = dumps(res712)   
        except:
            response_body = "watchedlisti dokemedim"

    elif querrry == 81:
        ''' q81, watchlist bir film cikarma. input: [ttid, userid], output: userid  watchlist.remove(ttid)'''
        try:
            res81 = ucollection.update({"_id":theUserId, "watchL":{"$in":[ttid]}},{"$pull":{"watchL":ttid}})
        except:
            response_body = "watch listen silemedim"

    elif querrry == 82:
        ''' q82, watchlistin hepsini silme. input: userid, output: watchL = [] '''
        try:
            res82 = ucollection.update({"_id":theUserId},{"$set":{"watchL":[]}})
        except:
            response_body = "watchlistin hepsini silemedim"
    
    elif querrry == 83:
        ''' q83, watchlistten bir grup film silme. input: userid, ttid&ttid&ttid, ... '''
        try:
            res83 = ucollection.update({"_id":theUserId, "watchL":{"$in":ttids}},{"$pullAll":{"watchL":ttids}})
        except:
            response_body = "watchlistten bir grup filmi silmeyi beceremedim."

    elif querrry == 91:
        ''' q91, watchedlist bir film cikarma. input: [ttid, userid], output: userid  watchedlist.remove(ttid)'''
        try:
            res91 = ucollection.update({"_id":theUserId, "watchedL":{"$in":[ttid]}},{"$pull":{"watchedL":ttid}})
        except:
            response_body = "watched listen silemedim"

    elif querrry == 92:
        ''' q92, watchedlistin hepsini silme. input: userid, output: watchedL = [] '''
        try:
            res92 = ucollection.update({"_id":theUserId},{"$set":{"watchedL":[]}})
        except:
            response_body = "watchedlistin hepsini silemedim"
    
    elif querrry == 93:
        ''' q93, watchedlistten bir grup film silme. input: userid, ttid&ttid&ttid, ... '''
        try:
            res93 = ucollection.update({"_id":theUserId, "watchedL":{"$in":ttids}},{"$pullAll":{"watchedL":ttids}})
        except:
            response_body = "watchedlistten bir grup filmi silmeyi beceremedim."

    elif querrry == 100:
        ''' q100, show all about a user. input userid '''
        try:
            res100 = ucollection.find({"_id":theUserId})
            response_body = dumps(res100)
        except:
            response_body = "kullaniciyi getiremedim"

    response_headers = [('Content-Type', 'text/plain'), ('Content-Length', str(len(response_body)))]
    start_response(status, response_headers)
    return [response_body]
