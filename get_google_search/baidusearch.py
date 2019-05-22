# ^_^ coding:utf8 ^_^
# open several baidu search results
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

headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36' }
print('baiduing...')
try:
    res = requests.get('https://www.baidu.com/s?wd=' + keyword, headers=headers)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, features='lxml')
    # garbage contents appear in result
    linkElems = list(filter(lambda x: '官网' not in x, soup.select('.t a')))
    greenElems = list(filter(lambda x: ':' not in x, soup.select('.c-showurl')))

    print('SEARCH RESULTS:\n')
    for j in range(min(5, len(linkElems))):
        print(linkElems[j].getText())
        try:
            print('   ' + greenElems[j].getText())
        except:
            pass
    input('enter to go to these links.')
    for j in range(min(5, len(linkElems))):
        webbrowser.open(linkElems[j].get('href'))
except Exception as exc:
    print(exc)
    input()
