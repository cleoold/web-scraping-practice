# ^_^ coding:utf8 ^_^
# open several google search results
## if no arguments are given, read content from clipboard
# (c) cos in may 2019

import sys
import webbrowser

import bs4
import pyperclip
import requests

if len(sys.argv) == 1:
    keyword = pyperclip.paste()
else:
    keyword = ' '.join(sys.argv[1:])

print('googling...')
try: 
    res = requests.get('https://google.com/search?q=' + keyword)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, features='lxml')
    # all matched search results (hyperlinks, and titles)
    ## <div class="r">
    ##      <a href="url...">...</a>
    linkElems = soup.select('.r a') # final all <a> elements within an element that has r class
    # green urls
    greenElems = soup.select('cite')
    print('SEARCHED RESULTS:')
    for j in range(min(5, len(linkElems))):
        print(linkElems[j].getText())
        print('  ' + greenElems[j].getText())
    input('enter to go to these links.')
    for j in range(min(5, len(linkElems))):
        webbrowser.open('https://google.com' + linkElems[j].get('href'))
except Exception as exc:
    print(exc)
    input()
