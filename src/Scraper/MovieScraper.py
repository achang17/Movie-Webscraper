from bs4 import BeautifulSoup
import requests
import logging

def testing_code(url):
    html_page = BeautifulSoup(requests.get(url).text, "html.parser")
    html_page.prettify()
    section_headers = html_page.body.find_all('h3')

    film_tag = [header for header in section_headers if header.span is not None and header.span.string == "Film"]
    if (len(film_tag) < 1):
        logging.warning("We cannot parse the format of this page")
        return

    table = film_tag[0].findNext('table')
    cols = [h.string for h in table.find_all('th')]

    title_idx = cols.index('Title\n')
    trs = table.find_all('tr')
    title_tds = [tr.find_all('td')[title_idx] for tr in trs if not len(tr.find_all('td')) < 1]
    movie_urls = [title.a['href'] for title in title_tds if not title.a is None]
    print(movie_urls)

def get_next_sibling(curr):
    while (curr.next_sibling == "\n"):
        curr = curr.next_sibling
    return curr

if __name__ == "__main__":
    testing_code('https://en.wikipedia.org/wiki/Jesse_Eisenberg')
    testing_code('https://en.wikipedia.org/wiki/Woody_Harrelson')
    testing_code('https://en.wikipedia.org/wiki/Dave_Franco')
    testing_code('https://en.wikipedia.org/wiki/Morgan_Freeman')
    print ("test code")

