from selenium import webdriver

driver = webdriver.Firefox()
driver.get("http://www.google.com/search?q=vanille+pannekoeken")
print driver.page_source
