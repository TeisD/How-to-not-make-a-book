from bs4 import BeautifulSoup
from requests import get
import urllib
from disqusapi import DisqusAPI
import re
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from threading import Thread
from googleapiclient.discovery import build

google_api_key = "AIzaSyDuV5zNTz8T7jwKf6X6MVDfjZQoDN1PQ6g"
google_cse_id = "011263252709623880646:fr2q4yl60bo"

disqus_secret_key = 'gEsLGMfIJ2Wy8Ft2nE84ANSoIJ61kLmNRQlRukgHEwfGb69ngZnRbyAhzPyeZv2G'
disqus_public_key = '7JIzndWon2HyoEnL8LUyaAIBLaDS8323wQ3qgbbAEPh3Hn4Ywgb3Cl04kJaWhmDW'

driver = webdriver.Firefox() # or add to your PATH
driver.implicitly_wait(5) # seconds

#url = "http://www.jamieoliver.com/recipes/chicken-recipes/blackened-chicken/" #jamieoliver.com
#url = "http://www.strandsofmylife.com/crispy-polenta-chicken-caesar-salad/" #wp
#url = "http://www.allconsuming.com.au/2013/11/26/chef-jamie-olivers-spiced-chicken-bacon-spinach-lentils/" #disqus
#url = "http://princesseatspeasoup.blogspot.com/2012/12/beef-steak-hoi-sin-prawn-noodle-bowls.html" #blogspot

tags = ['comment_content', 'comment-content', 'comment-body', 'comment_body', 'comments_content', 'comments-content', 'comments-body', 'comments_body']

def disqus(soup, url):
    print "DISQUS"
    comments = None

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
        result = get('https://disqus.com/api/3.0/threads/listPosts.json?api_key='+disqus_public_key+'&thread=link:'+urllib.quote(url)+'&forum='+disqus_id)
        comments = result.content

    return comments

def scrape(soup):
    print "SCRAPE"
    comments = None;

    container = soup.find('div', {'id':'comments'})
    if container is None: container = soup.find('div', {'class':'comments'})

    if container is not None:
        for tag in tags:
            print("searching for " + tag)
            comments = container.findAll('div',{'class':tag})
            if len(comments) > 0: break

        # we don't want links printed
        for comment in comments:
            if "http" in str(comment): comments.remove(comment)

    if comments is None: return comments
    elif len(comments) > 0: return comments
    else: return None

def deep(url):
    print "DEEP"
    comments = None;
    elements = []
    driver.get(url)

    for tag in tags:
        print("searching for " + tag)
        elements = driver.find_elements_by_class_name(tag)
        if len(elements) > 0:
            comments = []
            for element in elements:
                comments.append(element.text)
            break

    return comments

def search(keyword, tries):
    #http://stackoverflow.com/questions/37083058/programmatically-searching-google-in-python-using-custom-search
    url = 'https://www.googleapis.com/customsearch/v1?key={0}&cx={1}&q={2}&num={3}&fields=items(link)'.format(google_api_key, google_cse_id, keyword, tries)
    return json.loads(get(url).content)['items']

def get_comments(url):
    site = get(url, timeout = 5)
    soup = BeautifulSoup(site.content, 'html.parser')

    comments = disqus(soup, url)
    if comments is None: comments = scrape(soup)
    if comments is None: comments = deep(url)
    return comments

recipes = ["chicken tikka lentil, spinach & naam salad", "spicy cajun chicken smashed sweet potato & fresh corn salsa", "pork steaks hungarian pepper sauce & rice", "morrocan mussels tapenade toasties & cucumber salad"]

for recipe in recipes:
    print("Searching for: {0}").format(recipe)
    blogs = search(recipe, 3)
    for blog in blogs:
        comments = get_comments(blog['link'])
        if comments is not None:
            print comments
            break

driver.quit()
