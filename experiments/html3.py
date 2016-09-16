#load scripts on page before executing

from PIL import Image
from selenium import webdriver


driver = webdriver.Firefox() # or add to your PATH
driver.implicitly_wait(30) # seconds
driver.get('http://princesseatspeasoup.blogspot.com/2012/12/beef-steak-hoi-sin-prawn-noodle-bowls.html')
for element in driver.find_elements_by_class_name("comment-content"):
    print element.text

driver.quit()
