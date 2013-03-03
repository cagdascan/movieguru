import urllib2, re
    ##RocknRolla
    #filmId = 'tt1032755'
    ##Django Unchained Link
    #linko1 = 'http://www.imdb.com/title/tt1853728/'
    ##Matrix Link
    #linko2 = 'http://www.imdb.com/title/tt0133093/'
    
def fGet(filmId):
    #    ''' returns ... for a movie page from id in string format like tt******* '''
    linkMain = 'http://www.imdb.com/title/' + filmId + '/'
    linkKeys = linkMain + 'keywords?ref_=tt_stry_kw'
    data1 = urllib2.urlopen(linkMain).read()
    data11 = urllib2.urlopen(linkKeys).read()
        
    movieNameGE = r'<h1 class="header"> <span class="itemprop" itemprop="name">(.*)</span>'
    posterGE = r'src="(\w.*)"\n'# [0] itemprop="image" />\n</a>\.*</div>'
    durationGE = r'<time itemprop="duration" \w.*>(\w*) min'
    ratingGE = r'<meta itemprop="contentRating" content="\w.*?"/>(\w.*)</span>'#" />'
    genreGE = r'<span class="itemprop" itemprop="genre">(\w.*)</span></a>'
    userratingGE = r'<strong><span itemprop="ratingValue">(\w.*)</span></strong>'
    metascoreGE = r'provided by Metacritic.com" > (\w.*)/100' # /100
    firstplotGE = r'<p itemprop="description">\n(.*?)<'
    directorGE = r'Directors?:</h4>'
    writerGE = r'Writers?:</h4>'
    actorSplit = r'<td class="itemprop" itemprop="actor" itemscope itemtype="http://schema.org/Person">'
    actorGE = r'span class="itemprop" itemprop="name">(\w.*)</span>'
    dateGE = r'h4 class="inline">Release Date:</h4> (\d* \w* \d*)'
    keywordGE = r'<a href="/keyword/\w*/">(\w*)</a>\n</b></li><li><b class="keyword">'
    
    movieName = re.findall(movieNameGE, data1)[0]
    print movieName
    poster = re.findall(posterGE, data1)[0]
    print poster
    if len(re.findall(durationGE, data1))>0:
        print re.findall(durationGE,data1)[0]
        duration = re.findall(durationGE, data1)[0]
    else:
        duration = "N/A"
    if len(re.findall(ratingGE, data1))>0:
        print re.findall(ratingGE, data1)[0]
        rating = re.findall(ratingGE, data1)[0]
    else:
        rating = "N/A"
    genres = re.findall(genreGE, data1)
    userRating = re.findall(userratingGE, data1)[0]
    if len(re.findall(metascoreGE, data1))>0:
        metaRating = str(int(re.findall(metascoreGE, data1)[0])*1.0/100)
    else:
        metaRating = "N/A"
    if len(re.findall(firstplotGE,data1))>0:
        plotShort = re.findall(firstplotGE, data1)[0]
    else:
        plotShort = "N/A"
    directors = [] 
    writers = []
    actors = []
    if len(re.findall(dateGE, data1)) > 0:
        date = re.findall(dateGE, data1)[0]
    else:
        date = "N/A"
    keywords = re.findall(keywordGE,data11)
   
    if len(re.findall(directorGE,data1))>0: 
        temp = data1.split(re.findall(directorGE,data1)[0])
        temp = temp[1].split('</div>')
        temp = temp[0].split('itemprop="name">')
        if len(temp)>2:
            for i in range(1,len(temp),1):
                directors.append(temp[i].split('</span>')[0])
        else:
            directors.append(temp[1].split('</span>')[0])
    else:
        directors.append("N/A")
 
    if len(re.findall(writerGE,data1))>0:
        temp1 = data1.split(re.findall(writerGE,data1)[0])
        temp1 = temp1[1].split('</div>')
        temp1 = temp1[0].split('itemprop="name">') 
    
        if len(temp1)>2:
            for i in range(1,len(temp1),1):
                writers.append(temp1[i].split('</span>')[0])
        else:
            writers.append(temp1[1].split('</span>')[0])
    else:
        writers.append("N/A")
    
    
    temp = data1.split(actorSplit)
    for i in range(1,len(temp)):
        print i
        if len(re.findall(actorGE,temp[i]))>0:
            actors.append(re.findall(actorGE,temp[i])[0])
#        print ' ====================================='
#        print movieName
#        print ' '
#        print poster
#        print rating
#        print userRating
#        print genres
#        print plotShort
#        print directors
#        print actors
#        print date
#        print keywords
#        print '---------------------- DONE -----------------'
  
    return movieName, poster, rating, userRating, genres, plotShort, directors, actors, date, keywords 
    
    
    
    
    

      
    
#                95 min
#</time>

 
