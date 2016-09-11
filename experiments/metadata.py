import microdata #https://github.com/edsu/microdata
import urllib
import pprint

pp = pprint.PrettyPrinter(indent=1)

url = "http://ironchefshellie.com/2013/10/29/sizzling-beef-steak-hoi-sin-prawn-noodle-bowls/"
items = microdata.get_items(urllib.urlopen(url))

for item in items:
    #for itemtype in item.itemtype:
        #if str(itemtype) == "http://schema.org/CreativeWork":
    print(item.json())
