from selenium import webdriver
from BeautifulSoup import BeautifulSoup
import pandas as pd

driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
date=[] #List to store rating of the product
driver.get("https://www.michigan.gov/coronavirus/0,9753,7-406-98163-520743--,00.html")

content = driver.page_source
soup = BeautifulSoup(content)
for a in soup.findAll('a',href=True, attrs={'<strong>Confirmed COVID-19 ':' 2020</strong>'}):
date=a.find('div', attrs={'updated':'</strong'})

date.append(rating.text) 

print date

