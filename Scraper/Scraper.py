from bs4 import BeautifulSoup
import requests
import logging
import json

import os

from src.Scraper.Movie import Movie
from src.Scraper.Actor import Actor

'''
This function should take in the initial url and start the recursive scraping process.
Initial URL should be a wiki page to a movie, and we will scrape for actors pages, and for each actor page,
we will scrape for movie pages and repeat.

We will store list of actors and list of movies. Exit function when movies > 125 and actors > 250
'''
def scraper_starter(url):
    '''
    Outline:
    1. Keep lists actors_to_process and movies_to_process
    2. Keep lists scraped_actors and scraped_movies
    3. Given starting movie url
    4. scrape_movie to return movie_name, url, box_office, year, list of actors
    5. scrape_actor to return actor_name, age, movies, total_gross
    6. while actor_object < 250 or movie_object < 125 keep scraping
    '''

    scraped_actors = []
    scraped_movies = []

    actors_to_process = []
    movies_to_process = []

    first_movie = get_movie_page_data(url) # to return list with movie name, url, box_office, year, list of actors
    actors_to_process += first_movie[2]
    movie = Movie(first_movie[0], url, first_movie[1], first_movie[3], first_movie[4])

    scraped_movies.append(movie)

    while (len(scraped_actors) < 10 or len(scraped_movies) < 10):
        print(len(scraped_actors))
        print(len(scraped_movies))
        if (len(actors_to_process) == 0):
            logging.warning("We have run out of actor data to scrape")
            break
        else:
            while (len(actors_to_process) > 0):
                actor_url = actors_to_process.pop(0)
                print(actor_url)
                if ('https://' in actor_url):
                    logging.warning("This is not a valid URL")
                    break

                actor_page_data = get_actor_page_data('https://en.wikipedia.org'+actor_url)
                if (actor_page_data is not None):
                    movies_to_process += actor_page_data[2]
                    actor = Actor(actor_page_data[0], actor_page_data[1])
                    scraped_actors.append(actor)

        if (len(movies_to_process) == 0):
            logging.warning("We have run out of movie data to scrape")
            break
        else:
            while(len(movies_to_process) > 0):
                movie_url = movies_to_process.pop(0)
                if ('https://' in movie_url):
                    logging.warning("This is not a valid URL")
                    break
                movie_url = 'https://en.wikipedia.org' + movie_url
                movie_page_data = get_movie_page_data(movie_url) # to return list of actor name, age, movies
                if (movie_page_data is not None):
                    actors_to_process += movie_page_data[2]
                    movie = Movie(movie_page_data[0], movie_url, movie_page_data[1], movie_page_data[3], movie_page_data[4])
                    scraped_movies.append(movie)

        print('actors_to_process ')
        print(actors_to_process)
        print(len(actors_to_process))
        print('movies_to_process ')
        print(movies_to_process)
        print(len(movies_to_process))

        print('scraped_actors ')
        print(scraped_actors)
        print(len(scraped_actors))
        print('scraped_movies ')
        print(scraped_movies)
        print(len(scraped_movies))
        print()

        all_actors_and_movies = arrs_to_dict(scraped_movies, scraped_actors)
        with open('actors_and_movie.json', 'w') as out_file:
            json.dump(all_actors_and_movies, out_file, indent=2)

def arrs_to_dict(movies, actors):
    """
    Combines two lists (list of movie objects and list of actor objects) into a single dictionary that is indexed by
    the name of the object (movie or actor) and holds a formatted version of the object's information. The dictionary
    returned by this method would be JSON parseable.

    :param movies: list of movie objects holding name, url, actors
    :param actors: list of actor objects name, movies
    :return: a single dictionary containing both movie and actor data that is JSON parsable
    """
    combined_dict = {}
    for m in movies:
        combined_dict[m.get_name()] = m.to_dict()

    for a in actors:
        combined_dict[a.get_name()] = a.to_dict()

    return combined_dict

def get_movie_page_data(url):
    """
    Tries to parse a list of actors from the infobox. If we can parse the
    format of this actor's page and find a list of actors, return the name of the movie and a list of actors found on
    this page . Otherwise, logs error.

    :param url: The URL of a movie's wikipage
    :return: [name of movie, list of actor names, list of actor urls (starting with /wiki/<name of actor>), box_office, year]
    """
    print(url)
    page = requests.get(url).text
    html_page = BeautifulSoup(page, "html.parser")

    name = find_movie_name(url)
    box_office = find_box_office(url)
    year = find_movie_year(url)

    infobox = html_page.find(class_='infobox vevent')
    if (infobox is None):
        logging.warning("We cannot find actors from this movie page")
        return

    infobox = infobox.find_all('tr')
    for block in infobox:
        if ("Starring" in block.text):
            actor_urls = [ref.get('href') for ref in block.find_all('a')]
            actor_names = [ref.string for ref in block.find_all('a')]
            print(actor_urls)
            return name, actor_names, actor_urls, box_office, year


def find_box_office(url):
    html_page = BeautifulSoup(requests.get(url).text, "html.parser")
    html_page.prettify()
    info_box = html_page.find(class_='infobox vevent')
    if info_box is None:
        logging.warning("Cannot find box office of movie")
        return

    box_office = info_box.find('th', string="Box office")
    if box_office is None:
        logging.warning("Cannot find box office of movie")
        return

    box_office = box_office.find_next('td').contents[0]

    return parse_box_office(box_office)

def parse_box_office(bo):
    bo = bo.replace("$", "")
    bo = bo.replace(",", "")

    print(bo)
    if "million" in bo:
        bo = bo.split()
        #print(bo)
        bo[0] = float(bo[0])*1000000

    if "billion" in bo:
        bo = bo.split()
        bo[0] = float(bo[0])*1000000000

    print(int(bo[0]))
    return int(bo[0])


def get_actor_page_data(url): #actors_to_process, movies_to_process):
    """
    Tries to parse a list of movies from the Film table. If we can parse the
    format of this actor's page and find a list of movies, returns the name of an actor and also a list of movies found
    on this page. Otherwise, logs error.

    :param url: URL of an Actor's Wikipage
    :return: [name of actor, list of movie names, list of movie urls (starting with /wiki/<name of movie>)]
    """
    print(url)
    html_page = BeautifulSoup(requests.get(url).text, "html.parser")
    html_page.prettify()

    name = find_actor_name(url)

    section_headers = html_page.body.find_all('h3')
    film_tag = [header for header in section_headers if header.span is not None and header.span.string == "Film"]
    if (len(film_tag) < 1):
        logging.warning("We cannot find movies from this actor page")
        return

    table = film_tag[0].findNext('table')
    cols = [h.string for h in table.find_all('th')]
    title_idx = cols.index('Title\n') if 'Title\n' in cols else -1
    if (title_idx > 2):
        logging.warning("We cannot parse for movies on this actor page")
        return

    trs = table.find_all('tr')

    title_tds = [tr.find_all('td')[title_idx] for tr in trs if not len(tr.find_all('td')) < 1]
    movie_urls = [title.a['href'] for title in title_tds if title.a is not None]
    movie_names = [title.a.string for title in title_tds if title.a is not None]
    print(movie_urls)
    return name, movie_names, movie_urls


def find_actor_name(url):
    """
    Parses for name of the actor on wikipage. If we cannot understand the pattern of the page, we log an error.

    :param url: URL of the actor's wikipage
    :return: name of actor (as String or NavigableString)
    """
    html_page = BeautifulSoup(requests.get(url).text, "html.parser")
    html_page.prettify()
    bio = html_page.find(class_='infobox biography vcard')

    if bio is None:
        logging.warning("Cannot find name of Actor")
        return url

    if (bio.div is None):
        logging.warning("Cannot find name of Actor")
        return url

    return bio.div.string

def find_movie_name(url):
    """
    Parses for name of the movie on wikipage. If we cannot understand the pattern of the page, we log an error.

    :param url: URL of the movie's wikipage
    :return: name of movie (as String or NavigableString)
    """
    html_page = BeautifulSoup(requests.get(url).text, "html.parser")
    html_page.prettify()
    bio = html_page.find(class_='infobox vevent')

    if (bio is None):
        logging.warning("Cannot find name of Movie")
        return url
    return bio.th.string

def find_movie_year(url):
    html_page = BeautifulSoup(requests.get(url).text, "html.parser")
    html_page.prettify()
    info_box = html_page.find(class_='infobox vevent')

    if (info_box is None):
        logging.warning("Cannot find year of Movie")
        return

    year = info_box.find('div', string="Release date")
    if year is None:
        logging.warning("Cannot find year of movie at " + url)
        return

    year = year.find_next('li').contents
    if(len(year) < 3):
        logging.warning("Cannot find year of movie at " + url)
        return
    year = year[0]
    print(parse_year(year))
    return parse_year(year)

def parse_year(year):
    if year is None: return
    year = year.split()
    if len(year) < 2:
        logging.warning("Cannot find year of Movie")
        return
    return year[2]

def read_from_json(file):
    with open(file, 'r') as f:
        data_dict = json.load(f)
        return data_dict

if __name__ == "__main__":
    scraper_starter('https://en.wikipedia.org/wiki/Avengers:_Infinity_War')
    # get_actor_page_data('https://en.wikipedia.org/wiki/Laurence_Fishburne')
    # get_actor_page_data('https://en.wikipedia.org/wiki/Hugo_Weaving#Film')
    #find_actor_name('https://en.wikipedia.org/wiki/Jenny_Shakeshaft')
    # find_actor_name('https://en.wikipedia.org/wiki/Darius_Miles')
    #find_movie_year('https://en.wikipedia.org/wiki/How_I_Live_Now')
