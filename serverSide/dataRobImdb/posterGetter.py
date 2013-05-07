import pymongo, urllib2
from pymongo import MongoClient

conn = MongoClient("localhost", 27072)
db = conn.mov_db01_alpha

movs = db.movies02
results = movs.find({},{'_id':1, 'pLink':1})

for pic in results:
    print pic['_id']
    picname = pic['_id'] + '_poster' + pic['pLink'][-4:]
    f = open('posters/'+picname,'wb')
    f.write(urllib2.urlopen(pic['pLink']).read())
    f.close()

