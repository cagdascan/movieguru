import pymongo, urllib2, re, sys
from pymongo import MongoClient
import time
connection = MongoClient("localhost", 27072)

search_text = 'http://www.imdb.com/search/title?count=100&num_votes=5000,&porn=0&sort=moviemeter,asc&start=101&title_type=feature,documentary,video&user_rating=6.0,10'
from getter01 import *
from getter02 import *
from putter01 import *

liste = search2ids(search_text)
notDone = []
Done = []
for i in range(len(liste)):
    print 'putter should put it into db Completed: %'+str(i*1.0/len(liste)*100.0)
    if i%100 == 0:
        time.sleep(2)
    try:
        movieName, poster, rating, userRating, genres, plotShort, directors, actors, date, keywords = fGet(liste[i])
        dbPut01(liste[i], movieName, poster, rating, userRating, genres, plotShort, directors, actors, date, keywords)
        Done.append(liste[i])
    except:
        print "Unexpected error:", sys.exc_info()[0]
        notDone.append(liste[i])
        print liste[i]

f = open('unDoneList_movies01.txt','w')
f.write('\n'.join(x for x in notDone))
f.close()
