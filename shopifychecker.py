# -*- coding: utf-8 -*-
#!/python2.7
#Created by aj nicolas
import requests
from slacker import Slacker
from bs4 import BeautifulSoup

slack = Slacker('') # Enter in your Slack token

#While true to get a actual link
def linkfriendly():
    global url
    global r
    global soup

    while True:
        #Gets user shopify link
        try:
            url = raw_input('PASTE LINK HERE: ')
            headers ={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36'
                    '(KHTML, like Gecko) Chrome/56.0.2924.28 Safari/537.36'}

            r = requests.get(url+'.xml' ,headers=headers )
            soup = BeautifulSoup(r.content, 'html.parser')
            break
            # Handles exceptions
        except (requests.exceptions.MissingSchema,requests.exceptions.InvalidURL,requests.exceptions.ConnectionError,
            requests.exceptions.InvalidSchema,NameError) as e:
            print 'The link is not good!'

#Grabs handle text
def grabhandle():
    for handL in soup.findAll("handle"):
        return 'Handle: ' + handL.text

def grabdate():
    for created in soup.findAll("created-at"):
        return 'created: ' + created.text

def grabsku():
    for sku in soup.findAll("sku"):
        return 'sku: ' + sku.text

def grabprice():
    for price in soup.findAll("price"):
        return 'Price: ' + price.text

#Parses stock,sz name, and variants from shopify site
def grabszstk():
    global slack
    sz = []
    for size in soup.findAll("title")[1:]:
        # find text then append to a list
        sz.append(size)

    stk = []
    for stock in soup.findAll("inventory-quantity"):
        stk.append(stock)

    variants = []
    for variant in soup.findAll("id")[1:]:
        variants.append(variant)
    #Gets the total
    total = []
    for stock in soup.findAll("inventory-quantity"):
        total.append(int(stock.text))

    # formats the data
    fmt = '{:<5}{:<13}{:<10}{}'
    fmat = '{:<5}{:<13}{}'

    # zips the for lists together
    if len(stk) > 0:
        print(fmt.format('', 'Size', 'Stock', 'Variant'))
        for i, (sz, stk, variants) in enumerate(zip(sz, stk, variants)):
            print(fmt.format(i, sz.text, stk.text, variants.text))
        print 'TOTAL STOCK:', sum(total)
        slack.chat.post_message('#test', 'TOTAL STOCK: ') # Change #test to your channel name
        slack.chat.post_message('#test', sum(total)) # Change #test to your channel name

    #if stock wasn't found
    else:
        print 'STOCK WAS NOT FOUND'
        slack.chat.post_message('#test', 'STOCK WAS NOT FOUND') # Change #test to your channel name
        print(fmat.format('', 'size','variant'))
        for i, (sz,variants) in enumerate(zip(sz,variants)):
            print(fmat.format(i, sz.text, variants.text))

#Also bad formatting
def formattext():
    print '--' * 38
    print url
    print 'Press cmd + double click link to go to link!'
    try:
        print grabhandle() + ' | ' + grabdate() + ' \n' + grabprice() + ' \n' + grabsku()
        print ' '*38
        print grabszstk()
        print 'Press ctrl + z to exit'
    except TypeError:
        print "Try copying everything before the '?variant' \n or before the '?' in the link!".upper()

#While true statment for multiple link checks!
while True:
    if linkfriendly() is True:
        print linkfriendly()
    elif formattext() is True:
        print formattext()
