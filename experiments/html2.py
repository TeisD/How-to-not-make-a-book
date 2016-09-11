from bs4 import BeautifulSoup
from requests import get
import urllib
from disqusapi import DisqusAPI
import re

disqus_secret_key = 'gEsLGMfIJ2Wy8Ft2nE84ANSoIJ61kLmNRQlRukgHEwfGb69ngZnRbyAhzPyeZv2G'
disqus_public_key = '7JIzndWon2HyoEnL8LUyaAIBLaDS8323wQ3qgbbAEPh3Hn4Ywgb3Cl04kJaWhmDW'
tags = ['comments_content', 'comments-content', 'comment_content', 'comment-content', 'comment-body', 'comments-body', 'comment_body', 'comments_body']

url = "http://www.jamieoliver.com/recipes/chicken-recipes/blackened-chicken/" #jamieoliver.com
#url = "http://www.strandsofmylife.com/crispy-polenta-chicken-caesar-salad/" #wp
#url = "http://www.allconsuming.com.au/2013/11/26/chef-jamie-olivers-spiced-chicken-bacon-spinach-lentils/" #disqus
#url = "http://princesseatspeasoup.blogspot.com/2012/12/beef-steak-hoi-sin-prawn-noodle-bowls.html" #blogspot

site = get(url, timeout = 5)

soup = BeautifulSoup(site.content, 'html.parser')

# first: check if disqus exists for this page
scripts = soup.findAll('script')
disqus_id = None
for script in scripts:
    script = str(script)
    if "disqus_shortname" in script:
        for line in script.split("\n"):
            if "disqus_shortname=" in line.replace(" ", ""):
                start = line.index("=")+1
                end = line.index(";")
                clean =  line[start:end]
                disqus_id = clean.replace(" ", "")[1:-1]

if disqus_id != None:
    print disqus_id
    result = get('https://disqus.com/api/3.0/threads/listPosts.json?api_key='+disqus_public_key+'&thread=link:'+urllib.quote(url)+'&forum='+disqus_id)
    print result.content

exit()

container = soup.find('div', {'id':'comments'})
if container is None: container = soup.find('div', {'class':'comments'})

for tag in tags:
    comments = container.findAll('div',{'class':tag})
    if len(comments) > 0: break

# we don't want links printed
for comment in comments:
    if "http" in str(comment): comments.remove(comment)

for comment in comments:
    print(comment.text)
