from bs4 import BeautifulSoup
from requests import get
import urllib
from disqusapi import DisqusAPI
import json
from selenium import webdriver

disqus_secret_key = 'gEsLGMfIJ2Wy8Ft2nE84ANSoIJ61kLmNRQlRukgHEwfGb69ngZnRbyAhzPyeZv2G'
disqus_public_key = '7JIzndWon2HyoEnL8LUyaAIBLaDS8323wQ3qgbbAEPh3Hn4Ywgb3Cl04kJaWhmDW'

print("Starting webdriver...")
driver = webdriver.Chrome('/usr/lib/chromedriver') # or add to your PATH
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
        results = json.loads(get('https://disqus.com/api/3.0/threads/listPosts.json?api_key='+disqus_public_key+'&thread=link:'+urllib.quote(url)+'&forum='+disqus_id).content)["response"]
        if len(results) > 0:
            comments = []
            for comment in results:
                comments.append(comment["raw_message"])

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

    if comments is not None:
        if len(comments) > 0:
            ret_comments = []
            for comment in comments:
                ret_comments.append(comment.text)
            return ret_comments
        else: return None

    return comments

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
    results = []
    driver.get("https://www.google.com/search?q="+urllib.quote_plus(keyword))
    matches = driver.find_elements_by_css_selector('h3.r a')
    for match in matches:
        # get rid of pinterest
        link = match.get_attribute("href")
        if "pinterest" not in link: results.append(link)
        #match = match.find('a').get('href')[7:]
        #results.append(match[:match.index("&sa=")])

    return results[:tries]

def get_comments(url):
    site = get(url, timeout = 2)
    soup = BeautifulSoup(site.content, 'html.parser')

    comments = disqus(soup, url)
    if comments is None: comments = scrape(soup)
    if comments is None: comments = deep(url)
    return comments

recipes = ["blackened chicken & quinoa salad", "chicken tikka lentil, spinach & naam salad", "spicy cajun chicken smashed sweet potato & fresh corn salsa", "pork steaks hungarian pepper sauce & rice", "morrocan mussels tapenade toasties & cucumber salad"]

for recipe in recipes:
    comments = []
    count = 0
    print("Searching for: {0}").format(recipe)
    blogs = search(recipe, 5)
    for blog in blogs:
        blog_comments = get_comments(blog)
        if blog_comments is not None:
            print("Found {0} comments.").format(len(blog_comments))
            count += len(blog_comments)
            comments.append({"site": blog, "comments": blog_comments})
            if(count > 3): break #always fetch 3 comments
    print comments

driver.quit()
