## proj_nps.py
## Skeleton for Project 2 for SI 507
## ~~~ modify this file, but don't rename it ~~~
import requests
import json
from bs4 import BeautifulSoup
import sqlite3
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import plotly.graph_objects as go

CACHE_FNAME = 'movie_info.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()

except:
    CACHE_DICTION = {}

def get_unique_key(url):
  return url

def make_request_using_cache(url):
    unique_ident = get_unique_key(url)

    if unique_ident in CACHE_DICTION:
        # print("Getting cached data...")
        return CACHE_DICTION[unique_ident]

    else:
        # print("Making a request for new data...")
        resp = requests.get(url)
        CACHE_DICTION[unique_ident] = resp.text
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        return CACHE_DICTION[unique_ident]

html_content = make_request_using_cache('https://www.imdb.com/chart/top?ref_=nv_mv_250')
soup_main = BeautifulSoup(html_content, 'html.parser')

#film_n_link gives you movie name, ranking, and full link
film_list_prep = soup_main.find_all(class_ = 'posterColumn')
film_n_link = {}
for i in film_list_prep:
    # state_name = i.find('a').text
    url_suffix = i.find('a')['href']
    full_link = 'https://www.imdb.com' + url_suffix
    img_prep = i.find('img')
    movie_name = img_prep.get('alt', '')
    film_n_link[movie_name] = {}
    film_n_link[movie_name]['full_link'] = full_link
    film_n_link[movie_name]['movie_name'] = movie_name
    ranking = i.find("span").attrs['data-value']
    film_n_link[movie_name]['ranking'] = ranking

movie_director = []
movie_stars = []


for i in film_n_link:
    film_content = make_request_using_cache(film_n_link[i]['full_link'])
    film_content = BeautifulSoup(film_content, 'html.parser')
    js = json.loads("".join(film_content.find("script",{"type":"application/ld+json"}).contents))
    film_n_link[i]['average_rating'] = js['aggregateRating']['ratingValue']
    film_n_link[i]['year_published'] = js['datePublished'][0:4]
    try:
        film_n_link[i]['content_rating'] = js['contentRating']
    except:
        film_n_link[i]['content_rating'] = 'NA'



    for m in js['actor']:
        movie_stars.append([i,m['name']])

    try:
        movie_director.append([i,js['director']['name']])
    except:
        for n in js['director']:
            movie_director.append([i,n['name']])

DBNAME = 'movie_imdb.db'

def init_db():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    # Drop tables
    statement = '''
        DROP TABLE IF EXISTS 'movies';
    '''
    cur.execute(statement)

    statement = '''
        DROP TABLE IF EXISTS 'stars';
    '''
    cur.execute(statement)
    statement = '''
        DROP TABLE IF EXISTS 'directors';
    '''
    cur.execute(statement)

    statement = '''
        CREATE TABLE 'movies' (
                'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
                'Ranking' INTEGER,
                'Name' TEXT NOT NULL,
                'AverageRating' REAL,
                'ContentRating' TEXT NOT NULL,
                'Year' INTEGER
        );
    '''
    cur.execute(statement)


    statement = '''
        CREATE TABLE 'stars' (
                'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
                'MovieName' TEXT NOT NULL,
                'StarName' TEXT NOT NULL
        );
    '''
    cur.execute(statement)

    statement = '''
        CREATE TABLE 'directors' (
                'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
                'MovieName' TEXT NOT NULL,
                'DirectorName' TEXT NOT NULL
        );
    '''
    cur.execute(statement)

    conn.commit()
    conn.close()

def insert_stuff_movies():
    conn = sqlite3.connect(DBNAME)
    conn.text_factory = str
    cur = conn.cursor()

    for inst in film_n_link:

        insertion = (None, film_n_link[inst]['ranking'], inst, film_n_link[inst]['average_rating'], film_n_link[inst]['content_rating'], film_n_link[inst]['year_published'])
        statement = 'INSERT INTO "movies" '
        statement += 'VALUES (?, ?, ?, ?, ?, ?)'
        cur.execute(statement, insertion)


    conn.commit()
    conn.close()

def insert_stuff_directors():
    conn = sqlite3.connect(DBNAME)
    conn.text_factory = str
    cur = conn.cursor()

    for inst in movie_director:

        insertion = (None, inst[0], inst[1])
        statement = 'INSERT INTO "directors" '
        statement += 'VALUES (?, ?, ?)'
        cur.execute(statement, insertion)

    conn.commit()
    conn.close()

def insert_stuff_stars():
    conn = sqlite3.connect(DBNAME)
    conn.text_factory = str
    cur = conn.cursor()

    for inst in movie_stars:

        insertion = (None, inst[0], inst[1])
        statement = 'INSERT INTO "stars" '
        statement += 'VALUES (?, ?, ?)'
        cur.execute(statement, insertion)

    conn.commit()
    conn.close()

def plot_rating_count():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    # Drop tables

    statement = '''
        SELECT ContentRating, COUNT(*) FROM movies
        GROUP BY ContentRating
        ;
    '''
    output = cur.execute(statement)
    output = list(cur.fetchall())

    conn.commit()
    conn.close()

    rating_lst = []
    count_lst = []
    for i in output:
        rating_lst.append(i[0])
        count_lst.append(i[1])
    fig = go.Figure([go.Bar(x=rating_lst, y=count_lst, text=count_lst, textposition='auto')])
    fig.show()

def plot_actor_count():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    # Drop tables

    statement = '''
        SELECT StarName, COUNT(*) AS MovieCount
        FROM stars LEFT JOIN movies ON stars.MovieName = movies.Name
        GROUP BY StarName
        HAVING MovieCount>1
        ORDER BY MovieCount DESC
        ;
    '''
    output = cur.execute(statement)
    output = list(cur.fetchall())

    conn.commit()
    conn.close()

    star_lst = []
    count_lst = []
    for i in output:
        star_lst.append(i[0])
        count_lst.append(i[1])
    fig = go.Figure([go.Bar(x=star_lst, y=count_lst, text=count_lst, textposition='auto')])
    fig.show()

def plot_director_count():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    # Drop tables

    statement = '''
        SELECT DirectorName, AVG(AverageRating) AS MeanRating, COUNT(*) AS MovieNumber
        FROM directors LEFT JOIN movies ON directors.MovieName = movies.Name
        GROUP BY DirectorName
        HAVING MovieNumber > 1
        ORDER BY MeanRating DESC
        ;
    '''
    output = cur.execute(statement)
    output = list(cur.fetchall())

    conn.commit()
    conn.close()

    director_lst = []
    count_lst = []
    for i in output:
        director_lst.append(i[0])
        count_lst.append(i[1])
    fig = go.Figure([go.Bar(x=director_lst, y=count_lst, text=count_lst, textposition='auto')])
    fig.show()

def plot_year_count():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    # Drop tables

    statement = '''
        SELECT Year, COUNT(*) AS MovieCount
        FROM movies
        GROUP BY Year
        ORDER BY Year
        ;
    '''
    output = cur.execute(statement)
    output = list(cur.fetchall())

    conn.commit()
    conn.close()

    year_lst = []
    count_lst = []
    for i in output:
        year_lst.append(i[0])
        count_lst.append(i[1])
    fig = go.Figure(data=go.Scatter(x=year_lst, y=count_lst))
    fig.show()

def load_help_text():
    with open('help.txt') as f:
        return f.read()

# Part 3: Implement interactive prompt. We've started for you!
def interactive_prompt():
    help_text = load_help_text()
    response = ''
    while response != 'exit':
        response = raw_input('Enter a command: ')
        if response == 'help':
            print(help_text)
            continue
        elif response == 'directoraverage':
            print('Generating...')
            plot_director_count()
        elif response == 'yeartrend':
            print('Generating...')
            plot_year_count()
        elif response == 'actor':
            print('Generating...')
            plot_actor_count()
        elif response == 'contentrating':
            print('Generating...')
            plot_rating_count()
        elif response == 'exit':
            print('Bye...')
        else:
            print('Command not recognized...')

# Make sure nothing runs or prints out when this file is run as a module
if __name__=="__main__":
    init_db()
    insert_stuff_movies()
    insert_stuff_stars()
    insert_stuff_directors()
    interactive_prompt()
