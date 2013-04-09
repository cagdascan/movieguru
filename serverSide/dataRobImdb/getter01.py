import urllib2
import time
def page2ids(sText):
    ''' returns ids on a search page to a list'''
    page = urllib2.urlopen(sText).read()
    pageSections = page.split('<a href="/title/')
    tempList = []
    for i in range(1,len(pageSections),3):
        tempList.append(pageSections[i][0:9])
    return tempList

def search2ids(search_text):
    ''' returns all ids of a search with a result size of 100/page to a list '''
    main_search = urllib2.urlopen(search_text)
    main_html = main_search.read()
    forge = main_html.split('<div id="left">')
    borge = forge[1]
    forge = borge.split('<div id="right">')
    nosTitlesText = forge[0]
    nosTitlesText = nosTitlesText.split('of ')[1].split('titles')[0]
    nosTitles = int(nosTitlesText.split(',')[0] + nosTitlesText.split(',')[1])
    print nosTitles
    search_textL = search_text
    ids = []
    for i in range(1,nosTitles,100):
        print 'search to filIds completion '+ str(i*1.0/nosTitles*100)
        search_textL = search_textL.split('start=')[0] + 'start=' + str(i) + '&title_type=' + search_textL.split('&title_type=')[1]
        for j in page2ids(search_textL):
            ids.append(j)
        time.sleep(0.5)
    i = i + 100
    ssearch_textL = search_textL.split('start=')[0] + 'start=' + str(i) + '&title_type=' + search_textL.split('&title_type=')[1]
    for j in page2ids(ssearch_textL):
        ids.append(j) 
    return ids

#search_text = 'http://www.imdb.com/search/title?count=100&num_votes=5000,&porn=0&sort=moviemeter,asc&start=101&title_type=feature,documentary,video&user_rating=6.0,10'

