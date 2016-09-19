from requests import get
from bs4 import BeautifulSoup
import microdata #https://github.com/edsu/microdata
#https://www.scrapehero.com/how-to-prevent-getting-blacklisted-while-scraping/

page = get("http://www.google.com/search?q=vanille+pannekoeken", headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}).content
#page = open('google.html', 'r') # create new and empty existing

soup = BeautifulSoup(page, 'html.parser')
matches = soup.findAll(True, {'class':'r'})
for match in matches:
    match = match.find('a').get('href')[7:]
    match = match[:match.index("&sa=")]
    print match
