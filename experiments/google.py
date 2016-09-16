from requests import get
import microdata #https://github.com/edsu/microdata

page = get("https://www.google.com/search?q=vanille+pannekoeken")

f = open('google.html', 'w') # create new and empty existing
f.write(page.content)
f.close()

items = microdata.get_items(page.content)

for item in items:
    #for itemtype in item.itemtype:
        #if str(itemtype) == "http://schema.org/CreativeWork":
    print(item.json())
