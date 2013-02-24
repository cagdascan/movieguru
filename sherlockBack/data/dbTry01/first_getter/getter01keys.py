import urllib2
import time

f = open('test.dat','r')
allids = f.read().split('tt')
f.close()
keywordList = []
f = open('keywords.dat','w')

for i in range(1,len(allids)):
    print i*1.0/len(allids)
    page = urllib2.urlopen('http://www.imdb.com/title/tt'+allids[i]+'/keywords?ref_=tt_stry_kw').read()
    temp = page.split('<a href="/keyword/')
    print len(temp)
    if len(temp)>15:
        tempo = temp[1:16]
        for j in range(15):
            f.write(tempo[j].split('/">')[1].split('</a>')[0]+'\n')
    if i%500==0:
        time.sleep(2)


f.close()




