# -*- coding: utf-8 -*-
# grabs all shipgirl character images from http://wiki.joyme.com/blhx
# and download them
## PATH: from main page to each shipgirl page
#
#                                mainUrl
#            category0              |     ......          category14
#       --------------------------------------------------------------
#       |               |                                            |
#    shipgirl        shipgirl             ......                  shipgirl
#       |               |                                            |
#    -------         -------                                      -------
#    | ... |         | ... |                                      | ... |
#    images           images                                       images
## (c) cos in May 2019

import os
from random import randint

import bs4
import requests

_DEBUG = False

HEADERS = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36' }
mainUrl = r'http://wiki.joyme.com/blhx/%E9%A6%96%E9%A1%B5'

class blhxhsjDownload:
    def __init__(self, links2Shipgirls=[]):
        self.links2Shipgirls = links2Shipgirls
    def getUrls2Shipgirls(self):
        'gets links to each shipgirl'
        try:
            resMain = requests.get(mainUrl, headers=HEADERS)
            resMain.raise_for_status()
            soupMain = bs4.BeautifulSoup(resMain.text, features='lxml')
            if _DEBUG:
                with open('blhxhsj.html', 'w', encoding='utf-8') as src:
                    src.write(str(soupMain))
            # initialises list with keys [category]
            for each in soupMain.select('.MenuBox li'):
                self.links2Shipgirls.append([each.getText()])
            # gets urls to each shipgirl's page                    all urls inside con_0,1,...
            for j in range(len(self.links2Shipgirls)):                             #|
                links2aKind = [ [(each['title'], each['href']) , []] for each in soupMain.select('div[id="con_%d"] a' % j)\
                                if 'http' in each['href']]
                self.links2Shipgirls[j].append(links2aKind)           
        except Exception as exc:
            print(exc)
    def getUrls2Images(self):
        'gets links to every image after getting links to characters'
        'MUST BE RUN AFTER getUrls2Shipgirl'
        def getUrls2Images4OneCategory(category):
            # gets image links for each shipgirl page
            for correspondence in category[1]:
                # shipgirlUrl = correspondence[0][1]
                resShipgirl = requests.get(correspondence[0][1], headers=HEADERS)
                soupShipgirl = bs4.BeautifulSoup(resShipgirl.text, features='lxml')
                # getting character images
                links2Images = soupShipgirl.select('.tab_con img')
                # getting mini figures
                links2Minis = soupShipgirl.select('.qchar-container img')
                for each in links2Images + links2Minis:
                    correspondence[1].append({each['alt'] : each['src']})
                    print('got one shipgirl link' + '.' * randint(3, 6))
        try:
            for category in self.links2Shipgirls:
                getUrls2Images4OneCategory(category)
        except Exception as exc:
            print(exc)

    def writeUrls(self):
        with open('blhxhsj_img.txt', 'a', encoding='utf-8') as txt:
            txt.write(str(self.links2Shipgirls) + '\n\n\n')
    
    def download(self, separate_folders=False):
        for category in self.links2Shipgirls:
            os.makedirs(category[0], exist_ok=True)
            for correspondence in category[1]:
                shipgirlName = correspondence[0][0]
                if separate_folders:
                    os.makedirs(shipgirlName, exist_ok=True)
                for imageDict in correspondence[1]:
                    for key in imageDict.keys():
                        filePos = [os.path.join(category[0], key), os.path.join(category[0], shipgirlName, key)][separate_folders]
                        if not os.path.exists(filePos):
                            resImg = requests.get(imageDict[key], headers=HEADERS)
                            with open(filePos, 'wb') as file:
                                for chunk in resImg.iter_content(1000):
                                    file.write(chunk)
                            print('downloaded %s' % key)
                        else:
                            print('skipped an existing file.')

if __name__ == '__main__':
    print('SCRIPT STARTED.')
    x = blhxhsjDownload()
    x.getUrls2Shipgirls()
    x.getUrls2Images()
    if _DEBUG:
        x.writeUrls()
    elif not _DEBUG:
        x.download()
