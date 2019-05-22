# -*- coding: utf-8 -*-
# gets wallpapers from http://wiki.joyme.com/blhx/%E7%A2%A7%E8%93%9D%E5%BD%B1%E7%94%BB
# (c) cos in May 2019

import os
import requests
import bs4
import re

HEADERS = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36' }
mainUrl = r'http://wiki.joyme.com/blhx/%E7%A2%A7%E8%93%9D%E5%BD%B1%E7%94%BB'

resMain = requests.get(mainUrl, headers=HEADERS)
resMain.raise_for_status()
soupMain = bs4.BeautifulSoup(resMain.text, features='lxml')
for each in soupMain.select('.thumb .image'):
    link2ImageIndex = 'http://wiki.joyme.com' + each['href']
    # analysing each target url
    resImageIndex = requests.get(link2ImageIndex, headers=HEADERS)
    soupImageIndex = bs4.BeautifulSoup(resImageIndex.text, features='lxml')
    imageUrl = soupImageIndex.select('.fullMedia a')[0]['href']
    filename = os.path.basename(re.sub(r':', '/', each['href']))
    with open(filename, 'wb') as file:
        resImage = requests.get(imageUrl, headers=HEADERS)
        for chunk in resImage.iter_content(1000):
            file.write(chunk)
        print('downloaded ' + filename)
