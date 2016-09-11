from contextlib import closing
from urllib2 import urlopen
import html5lib #https://github.com/html5lib/html5lib-python

with closing(urlopen("http://www.strandsofmylife.com/crispy-polenta-chicken-caesar-salad/")) as f:
    dom = html5lib.parse(f, transport_encoding=f.info().getparam("charset"), treebuilder='dom')

print(dom)

for node in dom.getElementsByTagName('comment'):  # visit every node <bar />
    print node.toxml()
