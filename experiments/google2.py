from requests import get
from bs4 import BeautifulSoup
import microdata #https://github.com/edsu/microdata

#page = get("https://www.google.com/search?q=vanille+pannekoeken")
page = open('google.html', 'r') # create new and empty existing

soup = BeautifulSoup(page, 'html.parser')
matches = soup.findAll(True, {'class':'r'})
for match in matches:
    print match.find('a').get('href')[7:]
