#coding:utf-8
import pymongo
from pymongo import MongoClient
connection = MongoClient("localhost", 27017)
db = connection.test_database

from time import sleep
import urllib2
response = urllib2.urlopen('http://www.imdb.com/chart/top?ref_=nb_mv_3_chttp')
html = response.read()
#print html
forge = html.split('<table')
borge = forge[2].split('/table>')
#borge = forge.split('/table>')
forge = borge[0]
place = []
place_start='<b>'
place_end = '.</b>'
name = []
name_start = '/">'
name_end = '</a>'
imdbid = []
imdbid_start = '<a href="/title/'
imdbid_end = '/">'
year = []
year_start = '</a> ('
year_end = ')</font>'
forge = forge.split('<tr') 

for i in range(2,len(forge)):
    rowdata = forge[i]
    psi = rowdata.index(place_start)
    pfi = rowdata.index(place_end)
    place.append(rowdata[psi+3:pfi])
    nsi = rowdata.index(name_start)
    nfi = rowdata.index(name_end)
    name.append(rowdata[nsi+3:nfi])
    isi = rowdata.index(imdbid_start)
    ifi = rowdata.index(imdbid_end)
    imdbid.append(rowdata[isi+16:ifi])
    ysi = rowdata.index(year_start)
    yfi = rowdata.index(year_end)
    year.append(rowdata[ysi+6:yfi])
jsonss = []
for i in range(len(imdbid)):
    print i*'|' + '\n   of  \n' + 250*'|' + '\n' 
    jsonss.append(urllib2.urlopen('http://imdbapi.org/?ids='+imdbid[i]+'&type=json&plot=simple&episode=1&lang=en-US&aka=simple&release=simple&business=0&tech=0').read())
    sleep(1.331)

import ast
for i in range(len(jsonss)):     
    posts = db.posts
    post = ast.literal_eval(jsonss[1:-1])    
    post_id = posts.insert(post)

