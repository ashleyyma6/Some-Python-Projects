import time
import csv
from selenium import webdriver
import webbrowser

'''
open item URLs in csv  to increase its view count
'''

prefix = "https://xxx.com/item/"
item_links = []
with open('links.csv') as file:
    csvReader = csv.reader(file)
    for row in csvReader:
        index = row[0].index('item')+5 # get item id
        item_links.append(prefix+row[0][index:])

#driver = webdriver.Edge()
for link in item_links:
    # webdriver.get(link)
    webbrowser.open_new_tab(link)
    time.sleep(2) # to avoid server rejection
#driver.quit()
