from cgi import urlparse, escape
from pymongo import MongoClient
from bson.json_util import dumps

def application(environ, start_response):
    #response_body = 'The requested method was %s .' % environ['REQUEST_METHOD']
    #response_body = ['%s : %s is in Amsterdam' % (key, value) for key, value in sorted(environ.items())];
    #response_body = '\n'.join(response_body)
    #response_body = '[{"rating": 7.0, "genres": ["Comedy", "Romance"], "rated": "R", "filming_locations": "402 S. Myrtle, Monrovia, California, USA", "language": ["English"], "title": "American Pie", "runtime": ["95 min"], "poster": "http://img3.douban.com/lpic/s1317955.jpg", "imdb_url": "http://www.imdb.com/title/tt0163651/", "writers": ["Adam Herz"], "imdb_id": "tt0163651", "directors": ["Paul Weitz", "and 1 more credit"], "rating_count": 200458, "actors": ["Jason Biggs", "Chris Klein", "Thomas Ian Nicholas", "Alyson Hannigan", "Shannon Elizabeth", "Tara Reid", "Eddie Kaye Thomas", "Seann William Scott", "Eugene Levy", "Natasha Lyonne", "Mena Suvari", "Jennifer Coolidge", "Chris Owen", "Eric Lively", "Molly Cheek"], "plot_simple": "Four teenage boys enter a pact to lose their virginity by prom night.", "year": 1999, "country": ["USA"], "type": "M", "release_date": 19990709, "also_known_as": ["\u0410\u043c\u0435\u0440\u0438\u043a\u0430\u043d\u0441\u043a\u0438 \u043f\u0430\u0439"]}]'

    d = urlparse.parse_qsl(environ['QUERY_STRING'])
    #title = d.get('title', [''])[0]
    #genres = d.get('genre', [])
    #title = []
    genres = []
    year = []
    rating = []
    minrating =[]
    maxrating =[]
    for i in range(len(d)):
        if d[i][0] == 'genre':
            genres.append(d[i][1])
        if d[i][0] == 'year':
            year.append(d[i][1])
        if d[i][0] == 'rating':
            rating.append(d[i][1])
        if d[i][0] == 'minrating':
            minrating.append(d[i][1])
        if d[i][0] == 'maxrating':
            maxrating.append(d[i][1])
    #years = range(int(year[0]),int(year[1])+1)
    #ratings = range(int(float(rating[0])*10),int(float(rating[1])*10)+1)
    #ratings = [float(la)/10. for la in ratings] 
    connection = MongoClient("localhost", 27017)
    db = connection.test_database
    collection = db.posts
    if year[0] == "1800":
        year.append("1979")
    else:
        year.append(str(int(year[0])+9)) 
   
    #result = collection.find({"year":{"$gt": int(year[0])}, "rating":{"$gt": float(rating[0]), "$lte": float(rating[1])}, "genres": {"$in": genres}})
    #result = collection.find({"year":{"$gt": int(year[0])}, "rating":{"$gt": float(minrating[0]), "$lte": float(maxrating[0])}, "genres": {"$in": genres}})
    #result01 = collection.find({"year":{"$in": years}, "rating":{"$in": ratings}, "genres":{"$in": genres}})
    result02 = collection.find({"year":{"$gte": int(year[0]), "$lte": int(year[1])}, "rating":{"$gte": float(rating[0]), "$lte": float(rating[1])}, "genres":{"$in": genres}}) 
    resultJ = dumps(result02)
    #title = escape(title)
    #genres = [escape(genre) for genre in genres] 
    #response_body = response_body +'\n\n' + (str(title) or 'No title') + (str(genres) or 'No genres') + (str(year) or 'No Year')
    #response_body = str(d) + str(len(d))
    #response_body = "[{'rating': 9.3, 'genres': ['Crime', 'Drama'], 'rated': 'R', 'language': ['English'], 'title': 'The Shawshank Redemption', 'poster': 'http://img3.douban.com/lpic/s1311361.jpg', 'imdb_url': 'http://www.imdb.com/title/tt0111161/', 'directors': ['Frank Darabont'], 'also_known_as': ['Die Verurteilten'], 'imdb_id': 'tt0111161', 'country': ['USA'], 'filming_locations': 'Ashland, Ohio, USA', 'writers': ['Stephen King', 'Frank Darabont'], 'actors': ['Tim Robbins', 'Morgan Freeman', 'Bob Gunton', 'William Sadler', 'Clancy Brown', 'Gil Bellows', 'Mark Rolston', 'James Whitmore', 'Jeffrey DeMunn', 'Larry Brandenburg', 'Neil Giuntoli', 'Brian Libby', 'David Proval', 'Joseph Ragno', 'Jude Ciccolella'], 'plot_simple': 'Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.', 'year': 1994, 'runtime': ['142 min'], 'type': 'M', 'release_date': 19941014, 'rating_count': 894012}]"
    import json
    #response_body = '[{"rating": 9.3, "genres": ["Crime", "Drama"], "rated": "R", "filming_locations": "Ashland, Ohio, USA", "language": ["English"], "title": "The Shawshank Redemption", "runtime": ["142 min"], "poster": "http://img3.douban.com/lpic/s1311361.jpg", "imdb_url": "http://www.imdb.com/title/tt0111161/", "writers": ["Stephen King", "Frank Darabont"], "imdb_id": "tt0111161", "directors": ["Frank Darabont"], "rating_count": 894012, "actors": ["Tim Robbins", "Morgan Freeman", "Bob Gunton", "William Sadler", "Clancy Brown", "Gil Bellows", "Mark Rolston", "James Whitmore", "Jeffrey DeMunn", "Larry Brandenburg", "Neil Giuntoli", "Brian Libby", "David Proval", "Joseph Ragno", "Jude Ciccolella"], "plot_simple": "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.", "year": 1994, "country": ["USA"], "type": "M", "release_date": 19941014, "also_known_as": ["Die Verurteilten"]}]'

    #response_body = 'imdbapi([{"rating": 8.0, "genres": ["Animation", "Comedy", "Family", "Fantasy"], "rated": "G", "language": ["English", "French"], "title": "Ratatouille", "runtime": ["111 min"], "poster": "http://img3.douban.com/lpic/s2827137.jpg", "imdb_url": "http://www.imdb.com/title/tt0382932/", "writers": ["Brad Bird", "Jan Pinkava"], "imdb_id": "tt0382932", "directors": ["Brad Bird", "Jan Pinkava"], "rating_count": 259698, "actors": ["Patton Oswalt", "Ian Holm", "Lou Romano", "Brian Dennehy", "Peter Sohn", "Peter O'Toole", "Brad Garrett", "Janeane Garofalo", "Will Arnett", "Julius Callahan", "James Remar", "John Ratzenberger", "Teddy Newton", "Tony Fucile", "Jake Steinfeld"], "plot_simple": "Remy is a young rat in the French countryside who arrives in Paris, only to find out that his cooking idol is dead. When he makes an unusual alliance with a restaurant's new garbage boy, the culinary and personal adventures begin despite Remy's family's skepticism and the rat-hating world of humans.", "year": 2007, "country": ["USA"], "type": "M", "release_date": 20070629, "also_known_as": ["Delicious Ratatouille 3D"]}])';
    
    response_body = resultJ

    status='200 OK'
    output='Hello World!'




    response_headers1 = [('Content-type', 'application/json')]#, ('Content-Length', str(len(response_body)))]
    response_headers2 = [('Content-type', 'text/html'), ('Content-Length', str(len(response_body)))]
 
    start_response(status, response_headers1)

    return response_body

