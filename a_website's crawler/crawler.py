'''
crawl first 2 images of item in csv file

1. locate Edge browser history: C:\Users\XXX\AppData\Local\Microsoft\Edge\User Data\Default
2. manually search keywords in URL: xxx.com/item/id
3. put result in csv file
'''

import wget
import csv
import webbrowser

# direct item image link template found using browser inspect mode
prefix = "http://xxx.net/item/detail/orig/photos/" 
postfix1 = "_1.jpg"
postfix2 = "_2.jpg"
item_filename = []
# item_count = 0

with open('get.csv') as file:
    csvReader = csv.reader(file)
    for row in csvReader:
        index = row[0].index('item')+5
        # print(f'Item{item_count}:{row[0][index:]}')
        # item_count+=1
        item_filename.append(row[0][index:]+postfix1)
        # item_filename.append(row[0][index:]+postfix2)
# print(item_URL)

# open in browser
# for filename in item_filename:
#     webbrowser.open(prefix+filename, new=1)

#download
path = 'D:/save/'
for filename in item_filename:
    # print(prefix+filename)
    # print(path+filename)
    
    wget.download(prefix+filename, path+filename)
