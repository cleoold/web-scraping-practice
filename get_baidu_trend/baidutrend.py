# -*- coding: utf-8 -*-
# gets Baidu popular searches list and saves it to a file
# (c) cos in May 2019

import sys as _sys

import bs4 as _bs4 #and lxml
import requests as _requests

_DEBUG = False
_FILENAME = 'baidutrend.txt'

# fixes aligning problems for multibyte characters
_ljust = lambda s, n: s.ljust(n - (len(s.encode("gbk")) - len(s)))
_rjust = lambda s, n: s.rjust(n - (len(s.encode("gbk")) - len(s)))

# a page that always works for the program purpose
_url = "https://www.baidu.com/s?wd=sousuoredian"
_headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36' }
def baiduTrend():
    try:
        res = _requests.get(_url, headers=_headers)
        res.raise_for_status()
        soup = _bs4.BeautifulSoup(res.content, features='lxml')
        if _DEBUG:
            with open('baidutrend.html', 'w', encoding='utf-8') as src:
                src.write(str(soup))
        titles = soup.select('td table tbody tr td span a')           #|
        pops = soup.select('td table tbody tr .opr-toplist1-right')   #| place for updates
        length = len(titles)
        if length != len(pops): # one news matches one pop
            raise Exception('The number of entries don\'t match the number of popularities. Something must go wrong.')
        res = '     NEWS                 POP \n'
        for j in range(length):
            res += _ljust(titles[j].getText(), 20) + _rjust(pops[j].getText(), 10) + '\n'
        with open(_FILENAME, 'w') as file1:
            file1.write(res)
        return 0 # ok
    except Exception as exc:
        with open(_FILENAME, 'w') as file1:
            file1.write(exc)
        return 1 # an error occurred

if __name__ == '__main__':
    baiduTrend()